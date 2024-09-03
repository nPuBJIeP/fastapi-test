from fastapi import APIRouter, Depends

from app.errors.error_handler import ErrorHandler
from app.schemas import UserResponse, BalanceAddRequest, BalanceWithdrawRequest, BalanceTransferRequest, \
    TransferResponse
from app.services.user_service import UserService
import logging

balance_router = APIRouter(route_class=ErrorHandler)

logger = logging.getLogger("app")


@balance_router.post("/balance/add", response_model=UserResponse)
async def add_balance(data: BalanceAddRequest, user_service: UserService = Depends()):
    user = await user_service.add_balance(data)
    return UserResponse(user_id=user.id, balance=user.balance)


@balance_router.post("/balance/withdraw", response_model=UserResponse)
async def withdraw_balance(data: BalanceWithdrawRequest, user_service: UserService = Depends()):
    user = await user_service.withdraw_balance(data)
    return UserResponse(user_id=user.id, balance=user.balance)


@balance_router.post("/balance/transfer", response_model=[])
async def transfer_balance(data: BalanceTransferRequest, user_service: UserService = Depends()):
    user = await user_service.transfer_balance(data)
    return TransferResponse(sender={"user_id": user[0].id, "balance": user[0].balance},
                            recipient={"user_id": user[1].id, "balance": user[1].balance})


