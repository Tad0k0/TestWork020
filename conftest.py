import pytest
import pytest_asyncio

from dataclasses import dataclass
from typing import AsyncGenerator, Generator

from asyncio import get_event_loop

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from httpx import AsyncClient

from common.logger import logger
from config import settings


app_base_url = "http://127.0.0.1:8000/"



@pytest_asyncio.fixture(scope="function")
async def client() -> Generator:
    headers = {"Authorization": settings.api_key}
    logger.debug(headers)
    async with AsyncClient(base_url=app_base_url, headers=headers) as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.db_url)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session