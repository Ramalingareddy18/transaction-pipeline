from datetime import date as date_type
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TransactionRead(BaseModel):
    transaction_id: int
    date: Optional[date_type] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    category: Optional[str] = None
    account: Optional[str] = None
    transaction_type: Optional[str] = None
    month: Optional[int] = None
    year: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
