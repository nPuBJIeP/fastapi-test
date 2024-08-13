from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing_extensions import List

app = FastAPI()

# Конфигурация базы данных
db_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = db_client.user_balance_db


class BalanceTransferRequest(BaseModel):
    from_user_id: str
    to_user_id: str
    amount: float


class BalanceAddRequest(BaseModel):
    user_id: str
    amount: float


class BalanceWithdrawRequest(BaseModel):
    user_id: str
    amount: float


class CreateUserRequest(BaseModel):
    user_id: str
    amount: float


@app.post("/users/")
async def create_user(data: CreateUserRequest):
    new_user = {"user_id": data.user_id, "balance": data.balance}
    await db.balances.insert_one(new_user)
    return {"success"}


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = {"user_id": user_id}
    await db.balances.find_one(user)
    return {"success"}


@app.post("/balance/add")
async def add_balance(data: BalanceAddRequest):
    pass


@app.post("/balance/withdraw")
async def add_balance(data: BalanceWithdrawRequest):
    pass


@app.post("/balance/transfer")
async def add_balance(data: BalanceTransferRequest):
    pass
