from fastapi import APIRouter, Depends, HTTPException
from fastapi import status

from app.errors.exceptions import NotFoundError, InsufficientFunds, UserExistsError
from app.schemas import UserResponse, BalanceAddRequest, BalanceWithdrawRequest, BalanceTransferRequest
from app.service import UserService
import logging

balance_router = APIRouter()

logger = logging.getLogger("app")


@balance_router.post("/balance/add", response_model=UserResponse)
async def add_balance(data: BalanceAddRequest, user_service: UserService = Depends()):
    try:
        user = await user_service.add_balance(data)
        return UserResponse(user_id=user.id, balance=user.balance)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")


@balance_router.post("/balance/withdraw", response_model=UserResponse)
async def withdraw_balance(data: BalanceWithdrawRequest, user_service: UserService = Depends()):
    try:
        user = await user_service.withdraw_balance(data)
        return UserResponse(user_id=user.id, balance=user.balance)
    except UserExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except InsufficientFunds as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")


@balance_router.post("/balance/transfer", response_model=[])
async def transfer_balance(data: BalanceTransferRequest, user_service: UserService = Depends()):
    try:
        user = await user_service.transfer_balance(data)
        return [UserResponse(user_id=user[0].id, balance=user[0].balance),
                UserResponse(user_id=user[1].id, balance=user[1].balance)]
    except UserExistsError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except InsufficientFunds as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message)
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal error")
