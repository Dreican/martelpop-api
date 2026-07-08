class UserRepository:
    async def get(self, user_id: int):
        return await User.get(user_id)
