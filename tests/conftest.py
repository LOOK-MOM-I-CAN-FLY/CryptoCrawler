import pytest
from httpx import AsyncClient
from app.main import app
from app.database import engine
from app.models import Base

@pytest.fixture(scope='session', autouse=True)
async def prepare_db():
    # Создаём и сбрасываем схему перед тестами
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac