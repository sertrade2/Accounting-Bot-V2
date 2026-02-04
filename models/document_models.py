# models/document_models.py

from __future__ import annotations
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import date


# -----------------------------
# Line Item Model
# -----------------------------

class LineItem(BaseModel):
    description: Optional[str] = None
    unit: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    net_amount: Optional[float] = None
    vat_rate: Optional[float] = None
    vat_amount: Optional[float] = None
    total_amount: Optional[float] = None


# -----------------------------
# Party Model
# -----------------------------

class Party(BaseModel):
    name: Optional[str] = None
    idno: Optional[str] = None
    vat_code: Optional[str] = None
    address: Optional[str] = None
    bank: Optional[str] = None
    iban: Optional[str] = None


# -----------------------------
# Totals Model
# -----------------------------

class Totals(BaseModel):
    net_amount: Optional[float] = None
    vat_amount: Optional[float] = None
    total_amount: Optional[float] = None


# -----------------------------
# Metadata Model
# -----------------------------

class DocumentMetadata(BaseModel):
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    document_date: Optional[str] = None
    delivery_date: Optional[str] = None
    reference_number: Optional[str] = None
    contract_number: Optional[str] = None
    currency: Optional[str] = None


# -----------------------------
# Structured Accounting Model
# -----------------------------

class StructuredAccountingData(BaseModel):
    metadata: DocumentMetadata
    supplier: Party
    buyer: Party
    items: List[LineItem] = Field(default_factory=list)
    totals: Totals
