from fastapi import FastAPI, HTTPException, Depends
from fastapi import status
from app.errors.exceptions import UserExistsError, NotFoundError
from app.entity import User
from app.schemas import UserResponse, CreateUserRequest, BalanceAddRequest
from app.service import UserService
import logging

app = FastAPI()
logger = logging.getLogger("app")


@app.post("/users/", response_model=UserResponse)
async def create_user(data: CreateUserRequest, user_service: UserService = Depends()):
    new_user = User(user_id=data.user_id, balance=data.balance)
    try:
        await user_service.create_user(new_user)
        return UserResponse(user_id=data.user_id, balance=data.balance)
    except UserExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, user_service: UserService = Depends()):
    try:
        user = await user_service.get_user(user_id)
        return UserResponse(user_id=user.id, balance=user.balance)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")


#
# @app.post("/balance/add", response_model=UserResponse)
# async def add_balance(data: BalanceAddRequest, user_service: UserService = Depends()):
#     print('add balance')
#     user = await user_service.add_balance(data)
#     return user
#
# @app.post("/balance/withdraw")
# async def add_balance(data: BalanceWithdrawRequest):
#     pass
#
#
# @app.post("/balance/transfer")
# async def add_balance(data: BalanceTransferRequest):
#     pass
