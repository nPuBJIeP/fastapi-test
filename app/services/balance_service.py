from fastapi import Depends

from app.entity import User
from app.repository import UserMongoRepository
from app.schemas import BalanceAddRequest, BalanceWithdrawRequest, BalanceTransferRequest


class BalanceService:
    user_repo: UserMongoRepository

    def __init__(self, user_repo: UserMongoRepository = Depends()) -> None:
        self.user_repo = user_repo


    async def add_balance(self, data: BalanceAddRequest):
        return await self.user_repo.add_balance(data)

    async def withdraw_balance(self, data: BalanceWithdrawRequest):

        return await self.user_repo.withdraw_balance(data)

    async def transfer_balance(self, data: BalanceTransferRequest):
        # from_user = await self.user_repo.get_user()
        return await self.user_repo.transfer_balance(data)
