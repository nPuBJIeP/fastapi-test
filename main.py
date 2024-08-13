from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# Конфигурация базы данных
db_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = db_client.user_balance_db

class CreateUserBalance(BaseModel):
    user_id: str = Field(..., example="user123")
    balance: float = Field(default=0.0, ge=0.0, example=100.0)  # ge=0.0 гарантирует, что баланс не будет отрицательным


class UserBalance(BaseModel):
    user_id: str
    amount: float


class TransferBalance(BaseModel):
    from_user_id: str
    to_user_id: str
    amount: float


@app.get("/")
async def credit_balance():
    return {"ok"}


@app.post("/users/")
async def create_user_balance(data: CreateUserBalance):
    # Создание новой записи пользователя
    new_user = {"user_id": data.user_id, "balance": data.balance}
    await db.balances.insert_one(new_user)
    return {'success'}


@app.get("/users/{id}")
async def get_user_balance(id:str):
    print(id)
    # Создание новой записи пользователя
    user = {"user_id": id}
    await db.balances.find_one(user)

    return {'success'}


