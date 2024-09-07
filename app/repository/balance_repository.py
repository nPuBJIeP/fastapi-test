from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.depends import get_mongodb_client
from app.entity import User, BalanceAdd, BalanceWithdraw, BalanceTransfer, UserToUserTransfer
from app.errors.exceptions import UserNotFoundError, UserExistsError, InsufficientFundsError, DataBaseError


class BalanceMongoRepository:
    db: AsyncIOMotorClient

    def __init__(self, db: AsyncIOMotorClient = Depends(get_mongodb_client)) -> None:
        self.db: AsyncIOMotorDatabase = db.user_balance_db

    async def add_balance(self, balance_add_request: BalanceAdd):
        return await self.db.balances.update_one({"user_id": balance_add_request.user_id},
                                                 {"$inc": {"balance": balance_add_request.amount}})

    async def withdraw_balance(self, balance_withdraw_request: BalanceWithdraw):
        return await self.db.balances.update_one(
            {'user_id': balance_withdraw_request.user_id, "balance": {"$gt": balance_withdraw_request.amount}},
            {"$inc": {'balance': -balance_withdraw_request.amount}})

    async def transfer_balance(self, balance_transfer_request: BalanceTransfer):
        try:
            await self.db.balances.update_one({'user_id': balance_transfer_request.sender_id},
                                              {'$inc': {'balance': -balance_transfer_request.amount}})
        except Exception:
            raise DataBaseError()
        try:
            await self.db.balances.update_one({'user_id': balance_transfer_request.recipient_id},
                                              {'$inc': {'balance': balance_transfer_request.amount}})
        except Exception:
            await self.db.balances.update_one({'user_id': balance_transfer_request.sender_id},
                                              {'$inc': {'balance': balance_transfer_request.amount}})
            raise DataBaseError()

    async def delete_user(self, user_id) -> None:
        await self.db.balances.delete_one({'user_id': user_id})
