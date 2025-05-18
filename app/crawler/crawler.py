import asyncio
import httpx
import redis.asyncio as redis  # новый импорт!
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from ..database import get_db
from ..crud import create_or_update_price_record, get_coins

REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")

target_url = "https://api.coingecko.com/api/v3/coins/markets"
FETCH_INTERVAL = 60  # seconds

async def fetch_and_store(db: AsyncSession, cg_id: str, coin_id: int):
    params = {"vs_currency": "usd", "ids": cg_id}
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(target_url, params=params)
            resp.raise_for_status()
            data = resp.json()
            if not data:
                return
            d = data[0]
            record = {
                "recorded_at": datetime.now(timezone.utc).replace(second=0, microsecond=0),
                "price_usd": d['current_price'],
                "volume_24h": d.get('total_volume'),
                "price_change_24h": d.get('price_change_percentage_24h')
            }
            # upsert
            await create_or_update_price_record(db, coin_id, record)
    except Exception as e:
        print(f"Failed to fetch/store for {cg_id}: {e}")

async def acquire_lock(redis_conn, lock_name, expire=55):
    # Возвращает True, если удалось установить блокировку
    return await redis_conn.set(lock_name, "locked", ex=expire, nx=True)

async def worker():
    redis_conn = await redis.from_url(REDIS_URL)
    while True:
        if await acquire_lock(redis_conn, "cryptocrawler_lock"):
            try:
                async with get_db() as db:
                    coins = await get_coins(db)
                    tasks = [fetch_and_store(db, c.cg_id, c.id) for c in coins]
                    if tasks:
                        await asyncio.gather(*tasks)
            except SQLAlchemyError as dbe:
                print(f"DB Error: {dbe}")
            except Exception as e:
                print(f"Unknown error: {e}")
        else:
            print("Crawler is locked: another instance is working")
        await asyncio.sleep(FETCH_INTERVAL)
    await redis_conn.close()

'''async def worker():
    redis = await aioredis.create_redis_pool(REDIS_URL)
    while True:
        if await acquire_lock(redis, "cryptocrawler_lock"):
            try:
                async with get_db() as db:
                    coins = await get_coins(db)
                    tasks = [fetch_and_store(db, c.cg_id, c.id) for c in coins]
                    if tasks:
                        await asyncio.gather(*tasks)
            except SQLAlchemyError as dbe:
                print(f"DB Error: {dbe}")
            except Exception as e:
                print(f"Unknown error: {e}")
        else:
            print("Crawler is locked: another instance is working")
        await asyncio.sleep(FETCH_INTERVAL)
    redis.close()
    await redis.wait_closed()'''

if __name__ == "__main__":
    try:
        asyncio.run(worker())
    except (KeyboardInterrupt, SystemExit):
        pass
