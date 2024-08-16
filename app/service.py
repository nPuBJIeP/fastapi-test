from fastapi import Depends

from app.entity import User
from app.repository import UserMongoRepository
from app.schemas import BalanceAddRequest


class UserService:
    user_repo: UserMongoRepository

    def __init__(self, user_repo: UserMongoRepository = Depends()) -> None:
        self.user_repo = user_repo

    async def create_user(self, user: User):
        # todo check user exists
        # user_exists = await self.user_repo.user_exists(user)
        return await self.user_repo.create_user(user)

    async def get_user(self, user_id: int):
        return await self.user_repo.get_user(user_id)

    async def add_founds(self, data: BalanceAddRequest):
        return await self.user_repo.add_founds(data)
