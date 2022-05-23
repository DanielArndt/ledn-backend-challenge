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
    "/accounts", response_description="List all accounts", response_model=List[AccountModel]
)
async def list_accounts():
    accounts = await db["accounts"].find().to_list(1000)
    return accounts

