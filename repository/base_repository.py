from abc import ABC, abstractmethod

from sqlalchemy.engine import Result
from sqlalchemy import select, insert, delete, update
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
        res: Result = await self.session.execute(select(self.model))
        return res.scalars().all()


    async def find_one(self, pk: int):
        stmt = select(self.model).where(self.model.id==pk)
        res: Result = await self.session.execute(stmt)
        return res.scalar()

    async def find_one_by_filter(self, filters):
        stmt = select(self.model).filter_by(**filters)
        res: Result = await self.session.execute(stmt)
        return res.scalar()


    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res: Result = await self.session.execute(stmt)
        return res.scalar_one()


    async def delete_one(self, pk: int):
        await self.session.execute(delete(self.model).where(self.model.id==pk))


    async def update_one(self, pk: int, data: dict):
        stmt = update(self.model).where(self.model.id==pk).values(**data).returning(self.model)
        res: Result= await self.session.execute(stmt)
        return res.scalar()
