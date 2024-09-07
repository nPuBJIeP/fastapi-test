from fastapi import Depends
from app.entity import BalanceAdd, BalanceWithdraw, BalanceTransfer, UserToUserTransfer, User
from app.errors.exceptions import InsufficientFundsError
from app.repository.balance_repository import BalanceMongoRepository
from app.services.user_service import UserService


class BalanceService:
    balance_repo: BalanceMongoRepository
    user_service: UserService

    def __init__(
            self,
            balance_repo: BalanceMongoRepository = Depends(),
            user_service: UserService = Depends()
    ) -> None:
        self.balance_repo = balance_repo
        self.user_service = user_service

    async def add_balance(self, data: BalanceAdd):
        await self.balance_repo.add_balance(data)
        return await self.user_service.get_user(user_id=data.user_id)

    async def withdraw_balance(self, data: BalanceWithdraw):
        # можно без этого запроса, но тогда мы не знаем была ошибка из-за несуществующего юзера или из-за недостатка денег
        user = await self.user_service.get_user(user_id=data.user_id)
        if user.balance < data.amount:
            raise InsufficientFundsError()
        await self.balance_repo.withdraw_balance(data)
        return await self.user_service.get_user(user_id=data.user_id)

    async def transfer_balance(self, data: BalanceTransfer):
        sender = await self.user_service.get_user(data.sender_id)
        if sender.balance < data.amount:
            raise InsufficientFundsError()
        recipient = await self.user_service.get_user(data.recipient_id)
        await self.balance_repo.transfer_balance(data)
        sender_upd = await self.user_service.get_user(data.sender_id)
        recipient_upd = await self.user_service.get_user(data.recipient_id)
        return UserToUserTransfer(sender=User(user_id=sender_upd.id,
                                              balance=sender_upd.balance),
                                  recipient=User(user_id=recipient_upd.id,
                                                 balance=recipient_upd.balance))
