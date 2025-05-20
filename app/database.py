import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings

# создаём движок и локатор сессий
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# вот так FastAPI ждёт асинхронный генератор
async def get_db():
    session = AsyncSessionLocal()
    try:
        yield session       # здесь FastAPI отдаёт session в роут
    finally:
        await session.close()
