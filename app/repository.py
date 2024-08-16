from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.depends import get_mongodb_client
from app.entity import User
from app.schemas import BalanceAddRequest
from main import UserResponse


class UserMongoRepository:
    db: AsyncIOMotorClient

    def __init__(self, db: AsyncIOMotorClient = Depends(get_mongodb_client)) -> None:
        self.db = db.user_balance_db

    async def create_user(self, user: User):
        exists_user = await self.db.balances.find_one({"user_id": user.id})
        if exists_user:
            raise HTTPException(status_code=409, detail="User already exists.")
        db_user = {"user_id": user.id, "balance": user.balance}
        await self.db.balances.insert_one(db_user)
        response_user = UserResponse(user_id=user.id, balance=user.balance)
        return response_user

    async def get_user(self, user_id: int):
        user = await self.db.balances.find_one({"user_id": user_id})
        if user:
            return UserResponse(user_id=user['user_id'], balance=user['balance'])
        else:
            raise HTTPException(status_code=404, detail="User not found.")

    async def add_founds(self, data: BalanceAddRequest):
        print(data)
        user = await self.db.balances.find_one({"user_id": data.user_id})
        print(user)
        if user:
            upd_user = await self.db.balances.update_one({"user_id": data.user_id}, {"$inc": {"balance": data.amount}})
            print(upd_user)
        else:
            raise HTTPException(status_code=404, detail="User not found.")
