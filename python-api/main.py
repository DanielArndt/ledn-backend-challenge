import os
from typing import List

import motor.motor_asyncio
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials

import security
from models import AccountModel, TransactionModel, TransferModel
from services import AccountService, TransactionService

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.ledn


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
    account = await AccountService(db).get_account(email)
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
    balance = await AccountService(db).get_balance(email)
    return balance


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
    account_exists = await AccountService(db).is_valid_account(transaction.userEmail)
    if not account_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="userEmail: account not found",
        )
    inserted_id = await TransactionService(db).create_transaction(transaction)
    return inserted_id


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
    account_service = AccountService(db)
    from_account_exists = await account_service.is_valid_account(transfer.fromEmail)
    if not from_account_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fromEmail: account not found",
        )
    to_account_exists = await account_service.is_valid_account(transfer.toEmail)
    if not to_account_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="toEmail: account not found",
        )
    inserted_ids = await TransactionService(db).transfer(
        transfer.fromEmail, transfer.toEmail, transfer.amount, transfer.createdAt
    )
    return inserted_ids
