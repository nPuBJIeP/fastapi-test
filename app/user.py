from fastapi import Depends, APIRouter

from app.entity import User
from app.errors.error_handler import ErrorHandler
import logging
from app.schemas import UserResponse, CreateUserRequest
from app.service import UserService


user_router = APIRouter(route_class=ErrorHandler)
logger = logging.getLogger("app")


@user_router.post("/users", response_model=UserResponse)
async def create_user(data: CreateUserRequest, user_service: UserService = Depends()):
    new_user = User(user_id=data.user_id, balance=data.balance)
    await user_service.create_user(new_user)
    return UserResponse(user_id=data.user_id, balance=data.balance)


@user_router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, user_service: UserService = Depends()):
    user = await user_service.get_user(user_id)
    return UserResponse(user_id=user.id, balance=user.balance)


