from sqlalchemy.exc import IntegrityError

from core.schemas.task import (TaskCreate, TaskRead, TaskUpdate,
                               TaskUpdatePartial)
from exceptions import BadRequestException, NotFoundException
from utils.unitofwork import IUnitOfWork


class TaskService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_tasks(self) -> list[TaskRead]:
        async with self.uow:
            tasks: list = await self.uow.task.find_all()
            return [TaskRead.model_validate(task) for task in tasks]

    async def get_user_tasks(self, user_id: int) -> list[TaskRead]:
        async with self.uow:
            tasks: list = await self.uow.task.find_all_by_filter({"user_id": user_id})
            return [TaskRead.model_validate(task) for task in tasks]

    async def get_task(self, task_id: int) -> TaskRead:
        async with self.uow:
            task = await self.uow.task.find_one(task_id)
            if not task:
                raise NotFoundException(detail=f"Task not found")
            return TaskRead.model_validate(task)

    async def add_task(self, task: TaskUpdate) -> TaskRead:
        task_dict: dict = task.model_dump()
        async with self.uow:
            task_from_db = await self.uow.task.add_one(task_dict)
            task_to_return = TaskRead.model_validate(task_from_db)
            await self.uow.commit()
            return task_to_return

    async def delete_task(self, task_id: int) -> None:
        async with self.uow:
            task = await self.uow.task.find_one(task_id)
            if not task:
                raise NotFoundException(detail=f"Task not found")
            await self.uow.task.delete_one(task.id)
            await self.uow.commit()

    async def update_task(self, task_id: int, task: TaskCreate) -> TaskRead:
        task_dict: dict = task.model_dump()
        async with self.uow:
            task_obj = await self.uow.task.find_one(task_id)
            if not task_obj:
                raise NotFoundException(detail=f"Task not found")
            try:
                task_from_db = await self.uow.task.update_one(task_obj.id, task_dict)
            except IntegrityError:
                raise BadRequestException(detail="Bad request")
            task_to_return = TaskRead.model_validate(task_from_db)
            await self.uow.commit()
            return task_to_return

    async def update_task_partial(
        self, task_id: int, task: TaskUpdatePartial
    ) -> TaskRead:
        task_dict: dict = task.model_dump(exclude_unset=True)
        async with self.uow:
            task_obj = await self.uow.task.find_one(task_id)
            if not task_obj:
                raise NotFoundException(detail=f"Task not found")
            try:
                task_from_db = await self.uow.task.update_one(task_obj.id, task_dict)
            except IntegrityError:
                raise BadRequestException(detail="Bad request")
            task_to_return = TaskRead.model_validate(task_from_db)
            await self.uow.commit()
            return task_to_return
