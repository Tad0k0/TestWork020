from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import List


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"


class CreateTransaction(BaseModel):
    transaction_id: str = Field(pattern='^\d{1,6}$')
    user_id: str = Field(pattern='^user_\d{3}$')
    amount: float
    currency: Currency
    timestamp: datetime

class CreateTransactionResponse(BaseModel):
    task_id: str
    message: str


class Transaction(BaseModel):
    transaction_id: str = Field(pattern='^\d{1,6}$')
    amount: float


class GetStatisticsResponse(BaseModel):
    total_transactions: int
    average_transaction_amount: float
    top_transactions: List[Transaction]
