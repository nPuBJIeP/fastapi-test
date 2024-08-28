from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from app.depends import get_mongodb_client
from app.entity import User
from app.schemas import BalanceAddRequest, BalanceWithdrawRequest, BalanceTransferRequest
from app.errors.exceptions import NotFoundError, UserExistsError, InsufficientFunds, DataBaseError


class UserMongoRepository:
    db: AsyncIOMotorClient

    def __init__(self, db: AsyncIOMotorClient = Depends(get_mongodb_client)) -> None:
        self.db = db.user_balance_db

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
        print(len(user))
        if user is None:
            raise NotFoundError()
        return User(user_id=user['user_id'], balance=user['balance'])

    async def add_balance(self, data: BalanceAddRequest):
        user = await self.db.balances.find_one({"user_id": data.user_id})
        if user:
            add_balance_user = await self.db.balances.update_one({"user_id": data.user_id},
                                                                 {"$inc": {"balance": data.amount}})
            upd_user = await self.db.balances.find_one({"user_id": data.user_id})
            return User(user_id=upd_user['user_id'], balance=upd_user['balance'])
        else:
            raise NotFoundError()

    async def withdraw_balance(self, data: BalanceWithdrawRequest):
        user = await self.db.balances.find_one({'user_id': data.user_id})

        if user is None:
            raise UserExistsError()
        if user['balance'] < data.amount:
            raise InsufficientFunds()
        await self.db.balances.update_one({'user_id': data.user_id},
                                          {"$inc": {'balance': -data.amount}})
        upd_user = await self.db.balances.find_one({'user_id': data.user_id})
        return User(user_id=upd_user['user_id'], balance=upd_user['balance'])

    async def transfer_balance(self, data: BalanceTransferRequest):
        # users = await self.db.balances.find({"user_id": {"$in": [data.from_user_id, data.to_user_id]}})
        from_user = await self.db.balances.find_one({'user_id': data.from_user_id})
        to_user = await self.db.balances.find_one({'user_id': data.to_user_id})
        if from_user is None or to_user is None:
            raise NotFoundError()
        if from_user['balance'] < data.amount:
            raise InsufficientFunds()
        # транзацакции доступны только с 4.0 версии монго, у меня 2.7, поэтому пытаемся сделать фейковую атомарность(отъебись<3)
        try:
            await self.db.balances.update_one({'user_id': data.from_user_id}, {'$inc': {'balance': -data.amount}})
        except Exception:
            raise DataBaseError()#хз какую ошибку вернуть
        try:
            await self.db.balances.update_one({'user_id': data.to_user_id}, {'$inc': {'balance': data.amount}})
        except Exception:
            await self.db.balances.update_one({'user_id': data.from_user_id}, {'$inc': {'balance': data.amount}})
            raise DataBaseError()

        upd_from_user = await self.db.balances.find_one({'user_id': data.from_user_id})
        upd_to_user = await self.db.balances.find_one({'user_id': data.to_user_id})
        return [User(user_id=upd_from_user['user_id'], balance=upd_from_user['balance']),
                User(user_id=upd_to_user['user_id'], balance=upd_to_user['balance'])]
