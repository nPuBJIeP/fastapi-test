class UsersServices:
    def __init__(self, db):
        self.db = db

    async def create_user(self, user_data):
        print('ok')
        result = await self.db["users"].insert_one(user_data)
        return result
