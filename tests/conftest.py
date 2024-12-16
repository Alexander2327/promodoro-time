import asyncio

import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from core.config import settings
from core.models import Base

pytest_plugins = [

]

TEST_DATABASE_URL = settings.db.url


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    if settings.MODE == "TEST":
        engine = create_async_engine(TEST_DATABASE_URL, echo=True)

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
