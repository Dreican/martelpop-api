from app.features.users.dto.user_response import UserResponse
from app.features.users.mappers.role_mapper import RoleMapper
from app.features.users.models.user import User


class UserMapper:

    @staticmethod
    def to_response(user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            email=user.email,
            firstname=user.firstname,
            lastname=user.lastname,
            role=RoleMapper.to_response(user.role),
            is_active=user.is_active,
            avatar_url=(
                f"/files/{user.avatar.id}"
                if user.avatar
                else None
            )
        )

    @staticmethod
    def to_response_list(users: list[User]) -> list[UserResponse]:
        return [UserMapper.to_response(user) for user in users]


