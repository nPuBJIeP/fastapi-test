from fastapi import APIRouter, Depends

from app.errors.error_handler import ErrorHandler
from app.schemas import UserResponse, BalanceAddRequest, BalanceWithdrawRequest, BalanceTransferRequest, \
    BalanceTransferResponse
from app.services.balance_service import BalanceService
import logging

balance_router = APIRouter(route_class=ErrorHandler)

logger = logging.getLogger("app")


@balance_router.post("/balance/add", response_model=UserResponse)
async def add_balance(request: BalanceAddRequest, balance_service: BalanceService = Depends()):
    user = await balance_service.add_balance(request)
    return UserResponse(user_id=user.id, balance=user.balance)


@balance_router.post("/balance/withdraw", response_model=UserResponse)
async def withdraw_balance(request: BalanceWithdrawRequest, balance_service: BalanceService = Depends()):
    user = await balance_service.withdraw_balance(request)
    return UserResponse(user_id=user.id, balance=user.balance)


@balance_router.post("/balance/transfer", response_model=BalanceTransferResponse)
async def transfer_balance(request: BalanceTransferRequest, balance_service: BalanceService = Depends()):
    user = await balance_service.transfer_balance(request)
    return BalanceTransferResponse(
        sender={"user_id": user[0].id, "balance": user[0].balance},
        recipient={"user_id": user[1].id, "balance": user[1].balance},
    )
