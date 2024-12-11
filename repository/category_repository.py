from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category
from core.schemas.category import CategoryRead, CategoryCreate

class CategoryRepository(ABC):
    @abstractmethod
    async def get_categories(self) -> list[CategoryRead]:
        pass

    @abstractmethod
    async def get_category(self, category_id: int) -> CategoryRead:
        pass

    @abstractmethod
    async def create_category(self, category: CategoryCreate) -> CategoryRead:
        pass

    @abstractmethod
    async def delete_category(self, category_id: int) -> None:
        pass


class SqlAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_categories(self) -> Sequence[Category]:
        stmt = select(Category).order_by(Category.id)
        categories = await self.session.scalars(stmt)
        return categories.all()

    async def get_category(self, category_id: int) -> Category | None:
        return await self.session.get(Category, category_id)

    async def create_category(self, category: CategoryCreate) -> Category:
        category = Category(**category.model_dump())
        self.session.add(category)
        await self.session.commit()
        return category

    async def delete_category(self, category_id: int) -> None:
        category = await self.session.get(Category, category_id)
        await self.session.delete(category)
        await self.session.commit()
