from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from typing_extensions import List

from app.entity import User
from app.schemas import UserResponse, CreateUserRequest, BalanceAddRequest
from app.service import UserService

app = FastAPI()


@app.post("/users/", response_model=UserResponse)
async def create_user(data: CreateUserRequest, user_service: UserService = Depends()):
    new_user = User(user_id=data.user_id, balance=data.balance)
    # try:
    await user_service.create_user(new_user)
    return UserResponse(user_id=data.user_id, balance=data.balance)
    # except Exception:
    #     raise HTTPException(status_code=500, detail="Database exception.")


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, user_service: UserService = Depends()):
    user = await user_service.get_user(user_id)
    return user


#
@app.post("/balance/add", response_model=UserResponse)
async def add_balance(data: BalanceAddRequest, user_service: UserService = Depends()):
    print('add balance')
    user = await user_service.add_founds(data)
    return user
#
# @app.post("/balance/withdraw")
# async def add_balance(data: BalanceWithdrawRequest):
#     pass
#
#
# @app.post("/balance/transfer")
# async def add_balance(data: BalanceTransferRequest):
#     pass
