# extraction/schemas.py

from typing import Dict, Any

ALLOWED_CURRENCIES = {"MDL", "EUR", "USD", "RON", "RUB", "UAH", "GBP"}

DATE_FORMAT = "DD.MM.YYYY"

# Field-level extraction priority:
# 1) OCR-extracted tokens
# 2) Deterministic rules
# 3) LLM (must cite OCR span or return null)
FIELD_PRIORITY = {
    "money": ["ocr", "rules", "llm"],
    "dates": ["ocr", "rules", "llm"],
    "ids": ["ocr", "rules", "llm"],
    "names": ["ocr", "rules", "llm"],
    "tables": ["ocr", "rules", "llm"]
}

# Minimal JSON schema-like hints (used to validate LLM output)
LLM_SCHEMA_HINT: Dict[str, Any] = {
    "metadata": {
        "document_type": "string|null",
        "document_number": "string|null",
        "document_date": "string|null",
        "delivery_date": "string|null",
        "reference_number": "string|null",
        "contract_number": "string|null",
        "currency": "string|null"
    },
    "supplier": {
        "name": "string|null",
        "idno": "string|null",
        "vat_code": "string|null",
        "address": "string|null",
        "bank": "string|null",
        "iban": "string|null"
    },
    "buyer": {
        "name": "string|null",
        "idno": "string|null",
        "vat_code": "string|null",
        "address": "string|null",
        "bank": "string|null",
        "iban": "string|null"
    },
    "items": "array",
    "totals": {
        "net_amount": "number|null",
        "vat_amount": "number|null",
        "total_amount": "number|null"
    }
}
