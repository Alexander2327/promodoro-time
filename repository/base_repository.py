from abc import ABC, abstractmethod

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, pk: int):
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, pk: int):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session


    async def find_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()


    async def find_one(self, pk: int):
        result = await self.session.execute(select(self.model).where(self.model.id==pk))
        return result.scalar()


    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()


    async def delete_one(self, pk: int):
        await self.session.execute(delete(self.model).where(self.model.id==pk))
        await self.session.commit()
