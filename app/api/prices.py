from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional
from ..schemas import PriceListResponse, PriceRecordResponse
from ..crud import get_coin, get_price_records
from ..database import get_db

router = APIRouter(prefix="/api/v1/coins", tags=["prices"])

@router.get("/{coin_id}/prices", response_model=PriceListResponse)
async def read_prices(
    coin_id: int,
    from_dt: datetime = Query(..., alias="from"),
    to_dt: datetime = Query(..., alias="to"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    if not await get_coin(db, coin_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coin not found")
    count, items = await get_price_records(db, coin_id, from_dt, to_dt, limit, offset)
    return {"count": count, "list": items}

@router.get("/{coin_id}/prices/latest", response_model=PriceRecordResponse)
async def read_latest_price(
    coin_id: int,
    db: AsyncSession = Depends(get_db)
):
    if not await get_coin(db, coin_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coin not found")
    now = datetime.utcnow()
    count, items = await get_price_records(db, coin_id, now.replace(hour=0, minute=0, second=0), now, 1, 0)
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No price records")
    return items[0]