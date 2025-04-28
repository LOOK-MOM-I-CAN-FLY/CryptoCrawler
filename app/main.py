from fastapi import FastAPI
from .config import settings
from .database import engine
from .models import Base
from .api.coins import router as coins_router
from .api.prices import router as prices_router

app = FastAPI(title="CryptoMonitor API")

app.include_router(coins_router)
app.include_router(prices_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)