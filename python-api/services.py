import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder

from models import TransactionModel


class AppService:
    def __init__(self, db: motor.motor_asyncio.AsyncIOMotorDatabase):
        self.db = db


class AccountService(AppService):
    async def is_valid_account(self, email):
        account = await self.db["accounts"].count_documents({"email": email})
        return True if account else False

    async def get_account(self, email):
        return await self.db["accounts"].find_one({"email": email})

    async def get_balance(self, email):
        aggregate = (
            await self.db["transactions"]
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


class TransactionService(AppService):
    async def transfer(self, from_email, to_email, amount, created_at):
        from_transaction = TransactionModel(
            userEmail=from_email,
            amount=amount,
            type="send",
            createdAt=created_at,
        )
        to_transaction = TransactionModel(
            userEmail=to_email,
            amount=amount,
            type="receive",
            createdAt=created_at,
        )
        transactions = jsonable_encoder([from_transaction, to_transaction])
        response = await self.db["transactions"].insert_many(transactions)
        return [str(id) for id in response.inserted_ids]

    async def create_transaction(self, transaction: TransactionModel):
        transaction_jsonable = jsonable_encoder(transaction)
        new_transaction = await self.db["transactions"].insert_one(transaction_jsonable)
        return str(new_transaction.inserted_id)
