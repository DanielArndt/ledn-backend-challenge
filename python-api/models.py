from datetime import datetime
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


class TransactionModel(BaseModel):
    userEmail: str
    amount: int
    type: str
    createdAt: datetime


class TransferModel(BaseModel):
    fromEmail: str
    toEmail: str
    amount: int
    createdAt: datetime
