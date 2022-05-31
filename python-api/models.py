from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class AccountModel(BaseModel):
    firstName: str
    lastName: str
    country: str
    email: str
    dob: str
    mfa: Optional[str]
    createdAt: datetime
    updatedAt: datetime
    referredBy: Optional[str]


class TransactionType(str, Enum):
    SEND = "send"
    RECEIVE = "receive"
    CREDIT = "credit"
    DEBIT = "debit"


class TransactionModel(BaseModel):
    userEmail: str
    amount: int
    type: TransactionType
    createdAt: datetime


class TransferModel(BaseModel):
    fromEmail: str
    toEmail: str
    amount: int
    createdAt: datetime
