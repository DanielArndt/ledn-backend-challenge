from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


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
