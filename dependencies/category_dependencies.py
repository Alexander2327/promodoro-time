from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from repository.category_repository import CategoryRepository, SqlAlchemyCategoryRepository


def get_category_repository(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
) -> CategoryRepository:
    return SqlAlchemyCategoryRepository(session)