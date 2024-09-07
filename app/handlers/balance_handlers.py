from fastapi import APIRouter, Depends

from app.entity import BalanceAdd, BalanceWithdraw, BalanceTransfer
from app.errors.error_handler import ErrorHandler
from app.schemas import UserResponse, BalanceAddRequest, BalanceWithdrawRequest, BalanceTransferRequest, \
    BalanceTransferResponse
from app.services.balance_service import BalanceService
import logging

balance_router = APIRouter(route_class=ErrorHandler)

logger = logging.getLogger("app")


@balance_router.post("/balance/add", response_model=UserResponse)
async def add_balance(request: BalanceAddRequest, balance_service: BalanceService = Depends()):
    user = await balance_service.add_balance(BalanceAdd(user_id=request.user_id, amount=request.amount))
    return UserResponse(user_id=user.id, balance=user.balance)


@balance_router.post("/balance/withdraw", response_model=UserResponse)
async def withdraw_balance(request: BalanceWithdrawRequest, balance_service: BalanceService = Depends()):
    user = await balance_service.withdraw_balance(BalanceWithdraw(user_id=request.user_id, amount=request.amount))
    return UserResponse(user_id=user.id, balance=user.balance)


@balance_router.post("/balance/transfer", response_model=BalanceTransferResponse)
async def transfer_balance(request: BalanceTransferRequest, balance_service: BalanceService = Depends()):
    transfer_response = await balance_service.transfer_balance(
        BalanceTransfer(sender_id=request.sender_id, recipient_id=request.recipient_id, amount=request.amount))

    return BalanceTransferResponse(
        sender={"user_id": transfer_response.sender.id, "balance": transfer_response.sender.balance},
        recipient={"user_id": transfer_response.recipient.id, "balance": transfer_response.recipient.balance},
    )
