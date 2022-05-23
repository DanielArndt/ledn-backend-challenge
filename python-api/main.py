from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse

import motor.motor_asyncio
import os
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from bson import ObjectId


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


class TransactionModel(BaseModel):
    userEmail: str
    amount: int
    type: str
    createdAt: str

@app.get(
    "/transactions", response_description="List all transactions", response_model=List[TransactionModel],
)
async def list_transactions():
    transactions = await db["transactions"].find().to_list(1000)
    return transactions

@app.get(
    "/accounts/{email}", response_description="Get specific account", response_model=AccountModel,
)
async def get_account(email: str):
    account = await db["accounts"].find_one({"email": email})
    return account

@app.get(
    "/accounts/{email}/balance", response_description="Get the balance for an account", response_model=int
)
async def get_account_balance(email: str):
    transactions = await db["transactions"].find({"userEmail": email}).to_list(1000)

    # FIXME: there's probably a way to do this in one query, instead of two
    received_aggregate = await db["transactions"].aggregate([{"$match": {"userEmail": email, "type": "receive"}}, { "$group": { "_id" : None, "amount_received" : { "$sum": "$amount" } }}]).to_list(1000)
    sent_aggregate = await db["transactions"].aggregate([{"$match": {"userEmail": email, "type": "send"}}, { "$group": { "_id" : None, "amount_sent" : { "$sum": "$amount" } }}]).to_list(1000)

    amount_received = received_aggregate[0]["amount_received"]
    amount_sent = sent_aggregate[0]["amount_sent"]

    return amount_received - amount_sent

@app.post(
    "/transactions/", response_description="Create a transaction",
)
async def create_transaction():
    # TODO: Implement create transaction
    # - Debit and credit account
    # - Transfer between users
    return None
