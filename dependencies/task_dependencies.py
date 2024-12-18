from fastapi import Depends

from services.task_service import TaskService
from utils.unitofwork import IUnitOfWork, UnitOfWork


async def get_task_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> TaskService:
    return TaskService(uow)
