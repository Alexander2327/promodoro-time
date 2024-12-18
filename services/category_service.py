from core.schemas.category import CategoryCreate, CategoryRead
from exceptions import NotFoundException
from utils.unitofwork import IUnitOfWork


class CategoryService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_categories(self) -> list[CategoryRead]:
        async with self.uow:
            categories: list = await self.uow.category.find_all()
            return [CategoryRead.model_validate(category) for category in categories]

    async def get_category(self, category_id: int) -> CategoryRead:
        async with self.uow:
            category = await self.uow.category.find_one(category_id)
            if not category:
                raise NotFoundException(detail=f"Category not found")
            return CategoryRead.model_validate(category)

    async def add_category(self, category: CategoryCreate) -> CategoryRead:
        category_dict: dict = (
            category.model_dump()
        )  # подготовка данных для внесения в БД
        async with self.uow:  # вход в контекст (если выбьет с ошибкой, то изменения откатятся)
            category_from_db = await self.uow.category.add_one(category_dict)
            category_to_return = CategoryRead.model_validate(
                category_from_db
            )  # обработка полученных данных из БД для их возврата - делаем модель пидантик
            await self.uow.commit()  # это самый важный кусок кода, до этого коммита можно записать данные в 50 моделей, но если кто-то вылетит с ошибкой, все изменения откатятся! Если код дошёл сюда, то все прошло окей!
            return category_to_return

    async def delete_category(self, category_id: int) -> None:
        async with self.uow:
            category = await self.uow.category.find_one(category_id)
            if not category:
                raise NotFoundException(detail=f"Category not found")
            await self.uow.category.delete_one(category.id)
            await self.uow.commit()
