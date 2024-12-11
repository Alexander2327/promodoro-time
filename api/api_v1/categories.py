from fastapi import APIRouter, Depends
from starlette import status

from core.schemas.category import CategoryRead, CategoryCreate
from dependencies.category_dependencies import get_category_repository
from repository.category_repository import CategoryRepository

router = APIRouter(
    tags=["Categories"],
)


@router.get("/", response_model=list[CategoryRead], status_code=status.HTTP_200_OK)
async def get_categories(
        repository: CategoryRepository = Depends(get_category_repository),
    ):
    return await repository.get_categories()


@router.get("/{category_id}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
async def get_category(
        category_id: int,
        repository: CategoryRepository = Depends(get_category_repository),
    ):
    return await repository.get_category(category_id)


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def post_category(
        category_create: CategoryCreate,
        repository: CategoryRepository = Depends(get_category_repository),):
   return await repository.create_category(category_create)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
        category_id: int,
        repository: CategoryRepository = Depends(get_category_repository),
    ):
    return await repository.delete_category(category_id)
