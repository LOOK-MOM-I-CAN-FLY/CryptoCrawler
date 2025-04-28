from sqlalchemy import select, insert, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from .models import Coin, PriceRecord
from .schemas import CoinCreate
from datetime import datetime

# Coins
async def get_coins(db: AsyncSession):
    result = await db.execute(select(Coin))
    return result.scalars().all()

async def get_coin(db: AsyncSession, coin_id: int):
    result = await db.execute(select(Coin).where(Coin.id == coin_id))
    return result.scalar_one_or_none()

async def create_coin(db: AsyncSession, data: CoinCreate):
    stmt = insert(Coin).values(**data.dict()).returning(Coin)
    try:
        res = await db.execute(stmt)
        await db.commit()
        return res.scalar_one()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

async def delete_coin(db: AsyncSession, coin_id: int):
    stmt = delete(Coin).where(Coin.id == coin_id)
    res = await db.execute(stmt)
    if res.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coin not found")
    await db.commit()

# PriceRecords
async def get_price_records(db: AsyncSession, coin_id: int, start: datetime, end: datetime, limit: int, offset: int):
    stmt = select(PriceRecord).where(
        PriceRecord.coin_id == coin_id,
        PriceRecord.recorded_at >= start,
        PriceRecord.recorded_at <= end
    ).order_by(PriceRecord.recorded_at.desc()).limit(limit).offset(offset)
    res = await db.execute(stmt)
    items = res.scalars().all()
    return len(items), items

async def create_or_update_price_record(db: AsyncSession, coin_id: int, record: dict):
    record['coin_id'] = coin_id
    stmt = pg_insert(PriceRecord).values(**record)
    stmt = stmt.on_conflict_do_update(
        index_elements=[PriceRecord.coin_id, PriceRecord.recorded_at],
        set_=record
    )
    await db.execute(stmt)
    await db.commit()