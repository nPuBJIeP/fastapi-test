from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from app.depends import get_mongodb_client
from app.entity import User
from app.errors.exceptions import UserNotFoundError, UserExistsError


class UserMongoRepository:
    db: AsyncIOMotorClient

    def __init__(self, db: AsyncIOMotorClient = Depends(get_mongodb_client)) -> None:
        self.db: AsyncIOMotorDatabase = db.user_balance_db

    async def create_user(self, user: User):
        db_user = {"user_id": user.id, "balance": user.balance}
        await self.db.balances.insert_one(db_user)
        await self.db.balances.create_index([("user_id", 1)], unique=True)

    async def get_user(self, user_id: int):
        user = await self.db.balances.find_one({"user_id": user_id})
        if user is None:
            raise UserNotFoundError()
        return User(user_id=user['user_id'], balance=user['balance'])

    async def delete_user(self, user_id) -> None:
        await self.db.balances.delete_one({'user_id': user_id})
