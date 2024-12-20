from abc import ABC, abstractmethod

from core.models.db_helper import db_helper
from repository.category_repository import CategoryRepository
from repository.task_repository import TaskRepository
from repository.user_repository import UserRepository


class IUnitOfWork(ABC):
    category: CategoryRepository
    task: TaskRepository
    user: UserRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_factory = db_helper.session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.category = CategoryRepository(self.session)
        self.task = TaskRepository(self.session)
        self.user = UserRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
