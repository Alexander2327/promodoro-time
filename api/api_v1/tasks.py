from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from core.schemas.task import TaskCreate, TaskRead, TaskUpdate, TaskUpdatePartial
from dependencies.task_dependencies import get_task_service
from services.task_service import TaskService

router = APIRouter(
    tags=["Tasks"],
)

@router.get("/", response_model=list[TaskRead], status_code=status.HTTP_200_OK)
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)],
    ):
    return await task_service.get_tasks()

@router.get("/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def get_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)],
    ):
    return await task_service.get_task(task_id)

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def post_task(
        task: TaskCreate,
        task_service: Annotated[TaskService, Depends(get_task_service)],
    ):
    return await task_service.add_task(task)

@router.put("/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def put_task(
        task_id: int,
        task: TaskUpdate,
        task_service: Annotated[TaskService, Depends(get_task_service)],
    ):
    return await task_service.update_task(task_id, task)

@router.patch("/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def patch_task(
        task_id: int,
        task: TaskUpdatePartial,
        task_service: Annotated[TaskService, Depends(get_task_service)],
    ):
    return await task_service.update_task_partial(task_id, task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        task_service: Annotated[TaskService, Depends(get_task_service)],
    ):
    return await task_service.delete_task(task_id)
