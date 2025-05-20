from sqlalchemy import select, insert, delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from .models import Coin, PriceRecord
from .schemas import CoinCreate, PriceRecordCreate
from datetime import datetime

# Coins
async def get_coins(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Coin).offset(skip).limit(limit))
    return result.scalars().all()

async def get_coin(db: AsyncSession, coin_id: int):
    result = await db.execute(select(Coin).where(Coin.id == coin_id))
    return result.scalar_one_or_none()

async def create_coin(db: AsyncSession, coin: CoinCreate) -> Coin:
    db_coin = Coin(**coin.dict())
    db.add(db_coin)
    await db.commit()
    await db.refresh(db_coin)
    return db_coin

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

async def create_price_record(db: AsyncSession, price_record: PriceRecordCreate) -> PriceRecord:
    db_price_record = PriceRecord(**price_record.dict())
    db.add(db_price_record)
    await db.commit()
    await db.refresh(db_price_record)
    return db_price_record

async def get_latest_price(db: AsyncSession, coin_id: int) -> PriceRecord:
    result = await db.execute(
        select(PriceRecord)
        .where(PriceRecord.coin_id == coin_id)
        .order_by(PriceRecord.timestamp.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()