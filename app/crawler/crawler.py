import asyncio
import httpx
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..crud import create_or_update_price_record, get_coins

target_url = "https://api.coingecko.com/api/v3/coins/markets"

async def fetch_and_store(db: AsyncSession, cg_id: str, coin_id: int):
    params = {"vs_currency": "usd", "ids": cg_id}
    async with httpx.AsyncClient() as client:
        resp = await client.get(target_url, params=params, timeout=10)
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
        await create_or_update_price_record(db, coin_id, record)

async def worker():
    """
    Основной цикл воркера: каждую минуту получает список монет и сохраняет данные.
    """
    while True:
        # Создаем новую сессию БД на каждый проход
        async with get_db() as db:
            coins = await get_coins(db)
            tasks = [fetch_and_store(db, c.cg_id, c.id) for c in coins]
            if tasks:
                await asyncio.gather(*tasks)
        await asyncio.sleep(60)

if __name__ == "__main__":
    try:
        asyncio.run(worker())
    except (KeyboardInterrupt, SystemExit):
        pass