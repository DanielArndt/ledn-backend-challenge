import os
from typing import List

import motor.motor_asyncio
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials

import security
from models import AccountModel, TransactionModel, TransferModel

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.ledn


async def validate_account_exists(email: str):
    account = await db["accounts"].count_documents({"email": email})
    return True if account else False


@app.get(
    "/accounts",
    response_description="List the first 1000 accounts",
    response_model=List[AccountModel],
)
async def list_accounts(
    credentials: HTTPBasicCredentials = Depends(security.http_basic),
):
    security.validate_credentials(credentials)
    accounts = await db["accounts"].find().to_list(1000)
    return accounts


@app.get(
    "/transactions",
    response_description="List the first 1000 transactions",
    response_model=List[TransactionModel],
)
async def list_transactions(
    credentials: HTTPBasicCredentials = Depends(security.http_basic),
):
    security.validate_credentials(credentials)
    transactions = await db["transactions"].find().to_list(1000)
    return transactions


@app.get(
    "/accounts/{email}",
    response_description="Get details of an account",
    response_model=AccountModel,
)
async def get_account(
    email: str, credentials: HTTPBasicCredentials = Depends(security.http_basic)
):
    security.validate_credentials(credentials)
    account = await db["accounts"].find_one({"email": email})
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )
    return account


@app.get(
    "/accounts/{email}/balance",
    response_description="Get the balance for an account",
    response_model=int,
)
async def get_account_balance(
    email: str, credentials: HTTPBasicCredentials = Depends(security.http_basic)
):
    security.validate_credentials(credentials)
    aggregate = (
        await db["transactions"]
        .aggregate(
            [
                {"$match": {"userEmail": email}},
                {
                    "$group": {
                        "_id": {"type": "$type"},
                        "amount": {"$sum": "$amount"},
                    }
                },
            ]
        )
        .to_list(4)
    )
    sum_amount = {result["_id"]["type"]: result["amount"] for result in aggregate}

    return (
        sum_amount.get("receive", 0)
        + sum_amount.get("credit", 0)
        - sum_amount.get("send", 0)
        - sum_amount.get("debit", 0)
    )


@app.post(
    "/transactions",
    response_description="Create a transaction",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    transaction: TransactionModel,
    credentials: HTTPBasicCredentials = Depends(security.http_basic),
):
    security.validate_credentials(credentials)
    account_exists = await validate_account_exists(transaction.userEmail)
    if not account_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fromEmail: account not found",
        )
    transaction_jsonable = jsonable_encoder(transaction)
    new_transaction = await db["transactions"].insert_one(transaction_jsonable)
    return str(new_transaction.inserted_id)


@app.post(
    "/transfers",
    response_description="Create a transfer between two users",
    response_model=List[str],
    status_code=status.HTTP_201_CREATED,
)
async def create_transfer(
    transfer: TransferModel,
    credentials: HTTPBasicCredentials = Depends(security.http_basic),
):
    security.validate_credentials(credentials)
    from_account_exists = await validate_account_exists(transfer.fromEmail)
    if not from_account_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fromEmail: account not found",
        )
    to_account_exists = await validate_account_exists(transfer.toEmail)
    if not to_account_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="toEmail: account not found",
        )
    from_transaction = TransactionModel(
        userEmail=transfer.fromEmail,
        amount=transfer.amount,
        type="send",
        createdAt=transfer.createdAt,
    )
    to_transaction = TransactionModel(
        userEmail=transfer.toEmail,
        amount=transfer.amount,
        type="receive",
        createdAt=transfer.createdAt,
    )
    transactions = jsonable_encoder([from_transaction, to_transaction])
    response = await db["transactions"].insert_many(transactions)
    return [str(id) for id in response.inserted_ids]
