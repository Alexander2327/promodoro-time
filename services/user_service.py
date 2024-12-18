from sqlalchemy.exc import IntegrityError

from auth.utils import validate_password, hash_password
from core.schemas.user import UserRead, UserCreate, UserUpdatePartial
from exceptions.exception import (
    UnauthorizedException,
    NotFoundException,
    BadRequestException,
)
from utils.unitofwork import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def authenticate_user(self, username: str, password: str) -> UserRead:
        async with self.uow:
            user = await self.uow.user.find_one_by_filter({"username": username})
            if not user or not validate_password(password, str.encode(user.password)):
                raise UnauthorizedException(detail=f"Invalid username or password")
            return UserRead.model_validate(user)

    async def add_user(self, user: UserCreate) -> UserRead:
        user_dict: dict = user.model_dump()  # подготовка данных для внесения в БД
        user_dict["password"] = hash_password(user.password).decode()
        async with self.uow:  # вход в контекст (если выбьет с ошибкой, то изменения откатятся)
            user_from_db = await self.uow.user.add_one(user_dict)
            user_to_return = UserRead.model_validate(
                user_from_db
            )  # обработка полученных данных из БД для их возврата - делаем модель пидантик
            await self.uow.commit()  # это самый важный кусок кода, до этого коммита можно записать данные в 50 моделей, но если кто-то вылетит с ошибкой, все изменения откатятся! Если код дошёл сюда, то все прошло окей!
            return user_to_return

    async def update_user_partial(
        self, user_id: int, user: UserUpdatePartial
    ) -> UserRead:
        user_dict: dict = user.model_dump(exclude_unset=True)
        async with self.uow:
            user_obj = await self.uow.user.find_one(user_id)
            if not user_obj:
                raise NotFoundException(detail=f"User not found")
            try:
                user_from_db = await self.uow.user.update_one(user_obj.id, user_dict)
            except IntegrityError:
                raise BadRequestException(detail="Bad request")
            task_to_return = UserRead.model_validate(user_from_db)
            await self.uow.commit()
            return task_to_return
