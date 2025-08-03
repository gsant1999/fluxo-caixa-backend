from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
import uuid

class SaleBase(BaseModel):
    client_name: str
    operator_name: str
    product_type: str
    lives: int
    monthly_value: Decimal
    sale_date: date
    status: str = "Active"

class SaleCreate(SaleBase):
    pass

class SaleUpdate(BaseModel):
    client_name: Optional[str] = None
    operator_name: Optional[str] = None
    product_type: Optional[str] = None
    lives: Optional[int] = None
    monthly_value: Optional[Decimal] = None
    sale_date: Optional[date] = None
    status: Optional[str] = None

class Sale(SaleBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

