from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.collection import Collection

from app.depends import get_mongodb_client
from app.entity import User, BalanceAdd, BalanceWithdraw, BalanceTransfer
from app.errors.exceptions import UserNotFoundError, UserExistsError, InsufficientFundsError, DataBaseError


class UserMongoRepository:
    db: AsyncIOMotorClient

    def __init__(self, db: AsyncIOMotorClient = Depends(get_mongodb_client)) -> None:
        self.db: AsyncIOMotorDatabase = db.user_balance_db

    async def create_user(self, user: User):
        exists_user = await self.db.balances.find_one({"user_id": user.id})

        if exists_user:
            raise UserExistsError()

        db_user = {"user_id": user.id, "balance": user.balance}
        await self.db.balances.insert_one(db_user)
        response_user = User(user_id=user.id, balance=user.balance)
        return response_user

    async def get_user(self, user_id: int):
        user = await self.db.balances.find_one({"user_id": user_id})
        if user is None:
            raise UserNotFoundError()
        return User(user_id=user['user_id'], balance=user['balance'])

    async def delete_user(self, user_id) -> None:
        await self.db.balances.delete_one({'user_id': user_id})
