from fastapi import Depends

from app.entity import User
from app.repository.user_repository import UserMongoRepository


class UserService:
    user_repo: UserMongoRepository

    def __init__(self, user_repo: UserMongoRepository = Depends()) -> None:
        self.user_repo = user_repo

    async def create_user(self, user: User):
        return await self.user_repo.create_user(user)

    async def get_user(self, user_id: int):
        return await self.user_repo.get_user(user_id)

    async def delete_user(self, user_id: int) -> None:
        return await self.user_repo.delete_user(user_id)
