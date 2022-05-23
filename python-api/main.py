from fastapi import FastAPI
import motor.motor_asyncio
import os
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.ledn


@app.get("/")
def read_root():
    return {"Hello": "World"}


class AccountModel(BaseModel):
    firstName: str
    lastName: str
    country: str
    email: str
    dob: str
    mfa: Optional[str]
    createdAt: str
    updatedAt: str
    referredBy: Optional[str]

@app.get(
    "/accounts", response_description="List all accounts", response_model=List[AccountModel],
)
async def list_accounts():
    accounts = await db["accounts"].find().to_list(1000)
    return accounts

@app.get(
    "/accounts/{email}", response_description="Get specific account", response_model=AccountModel,
)
async def get_account(email: str):
    account = await db["accounts"].find_one({"email": email})
    return account

@app.get(
    "/accounts/{email}/balance", response_description="Get the balance on an account",
)
async def get_account_balance(email: str):
    # TODO: Implement get account balance
    return email

@app.post(
    "/transactions/", response_description="Create a transaction",
)
async def create_transaction():
    # TODO: Implement create transaction
    # - Debit and credit account
    # - Transfer between users
    return None
