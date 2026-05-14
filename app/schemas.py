from datetime import date as DateType
from typing import Literal

from pydantic import BaseModel, Field


TransactionType = Literal["income", "expense", "transfer"]


class TransactionCreate(BaseModel):
    date: DateType
    type: TransactionType
    category: str = Field(min_length=1)
    amount: float = Field(gt=0)
    note: str | None = None


class TransactionUpdate(BaseModel):
    date: DateType | None = None
    type: TransactionType | None = None
    category: str | None = Field(default=None, min_length=1)
    amount: float | None = Field(default=None, gt=0)
    note: str | None = None


class Transaction(TransactionCreate):
    id: int

    model_config = {
        "from_attributes": True
    }
