# extraction/structured_extractor.py

import logging
from typing import Optional, Dict, Any

from models.document_models import (
    StructuredAccountingData,
    DocumentMetadata,
    Party,
    LineItem,
    Totals
)

from .rule_extractors import RuleExtractors
from .table_parser import TableParser
from .normalizers import Normalizers
from .crosslink import CrossLinker
from .llm_extractor import LLMExtractor


logger = logging.getLogger(__name__)


class StructuredAccountingExtractor:

    def __init__(self, llm_callable=None):
        self.llm = LLMExtractor(llm_callable)

    async def extract(
        self,
        ocr_text: str,
        document_type: Optional[str] = None
    ) -> StructuredAccountingData:

        # -------------------------
        # 1) Deterministic extraction
        # -------------------------
        doc_number = RuleExtractors.extract_document_number(ocr_text)
        doc_date = RuleExtractors.extract_first_date(ocr_text)
        currency = RuleExtractors.extract_currency(ocr_text)
        totals = RuleExtractors.extract_totals(ocr_text)
        iban = RuleExtractors.extract_iban(ocr_text)

        items = TableParser.parse_items(ocr_text)
        totals = CrossLinker.reconcile_totals(items, totals)

        # -------------------------
        # 2) LLM enrichment (optional)
        # -------------------------
        llm_data: Optional[Dict[str, Any]] = await self.llm.extract(ocr_text, document_type)

        # -------------------------
        # 3) Merge with priority (rules → LLM only fills nulls)
        # -------------------------
        metadata = DocumentMetadata(
            document_type=document_type,
            document_number=doc_number or _safe_get(llm_data, "metadata", "document_number"),
            document_date=doc_date or _safe_get(llm_data, "metadata", "document_date"),
            delivery_date=_norm_date(_safe_get(llm_data, "metadata", "delivery_date")),
            reference_number=_safe_get(llm_data, "metadata", "reference_number"),
            contract_number=_safe_get(llm_data, "metadata", "contract_number"),
            currency=currency or _norm_cur(_safe_get(llm_data, "metadata", "currency"))
        )

        supplier = _party_from_llm(llm_data, "supplier", iban_override=iban)
        buyer = _party_from_llm(llm_data, "buyer")

        items_models = [LineItem(**_normalize_item(i)) for i in (items or _safe_get(llm_data, "items") or [])]

        totals_model = Totals(
            net_amount=totals.get("net_amount") or _norm_money(_safe_get(llm_data, "totals", "net_amount")),
            vat_amount=totals.get("vat_amount") or _norm_money(_safe_get(llm_data, "totals", "vat_amount")),
            total_amount=totals.get("total_amount") or _norm_money(_safe_get(llm_data, "totals", "total_amount")),
        )

        result = StructuredAccountingData(
            metadata=metadata,
            supplier=supplier,
            buyer=buyer,
            items=items_models,
            totals=totals_model
        )

        logger.info("Structured extraction completed")
        return result


# -------------------------
# Helpers
# -------------------------

def _safe_get(d: Optional[Dict[str, Any]], *path):
    cur = d or {}
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def _norm_money(v):
    return Normalizers.normalize_money(str(v)) if v is not None else None


def _norm_date(v):
    return Normalizers.normalize_date(str(v)) if v is not None else None


def _norm_cur(v):
    return Normalizers.normalize_currency(str(v)) if v is not None else None


def _party_from_llm(llm_data, key: str, iban_override: Optional[str] = None):
    name = _safe_get(llm_data, key, "name")
    idno = _safe_get(llm_data, key, "idno")
    vat_code = _safe_get(llm_data, key, "vat_code")
    address = _safe_get(llm_data, key, "address")
    bank = _safe_get(llm_data, key, "bank")
    iban = iban_override or _safe_get(llm_data, key, "iban")

    return Party(
        name=name,
        idno=idno,
        vat_code=vat_code,
        address=address,
        bank=bank,
        iban=iban
    )


def _normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "description": item.get("description"),
        "unit": item.get("unit"),
        "quantity": _norm_money(item.get("quantity")) if item.get("quantity") is not None else None,
        "unit_price": _norm_money(item.get("unit_price")) if item.get("unit_price") is not None else None,
        "net_amount": _norm_money(item.get("net_amount")) if item.get("net_amount") is not None else None,
        "vat_rate": _norm_money(item.get("vat_rate")) if item.get("vat_rate") is not None else None,
        "vat_amount": _norm_money(item.get("vat_amount")) if item.get("vat_amount") is not None else None,
        "total_amount": _norm_money(item.get("total_amount")) if item.get("total_amount") is not None else None,
    }
