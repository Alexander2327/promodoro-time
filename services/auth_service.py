from auth.utils import validate_password, hash_password
from core.schemas.user import UserRead, UserCreate
from exceptions.exception import UnauthorizedException
from utils.unitofwork import IUnitOfWork


class AuthService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def authenticate_user(self, username: str, password: str) -> UserRead:
        async with self.uow:
            user = await self.uow.user.find_one_by_filter({"username": username})
            if not user or not validate_password(password, str.encode(user.password)):
                raise UnauthorizedException(detail=f"Invalid username or password")
            return UserRead.model_validate(user)

    async def add_user(self, user: UserCreate) -> UserRead:
        user_dict: dict = user.model_dump()
        user_dict["password"] = hash_password(user.password).decode()
        async with self.uow:
            user_from_db = await self.uow.user.add_one(user_dict)
            user_to_return = UserRead.model_validate(user_from_db)
            await self.uow.commit()
            return user_to_return
