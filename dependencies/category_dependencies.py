from fastapi import Depends

from services.category_service import CategoryService
from utils.unitofwork import IUnitOfWork, UnitOfWork


async def get_category_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> CategoryService:
    return CategoryService(uow)