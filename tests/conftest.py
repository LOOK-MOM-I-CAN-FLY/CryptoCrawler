import pytest
from httpx import AsyncClient
from app.main import app
from app.database import engine
from app.models import Base
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture(scope="session")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as session:
        yield session

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac