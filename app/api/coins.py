from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..schemas import CoinCreate, CoinResponse
from ..crud import get_coins, create_coin, delete_coin, get_coin
from ..database import get_db

router = APIRouter(prefix="/api/v1/coins", tags=["coins"])

@router.get("/", response_model=List[CoinResponse])
async def list_coins(db: AsyncSession = Depends(get_db)):
    return await get_coins(db)

@router.post("/", response_model=CoinResponse, status_code=status.HTTP_201_CREATED)
async def add_coin(
    coin_in: CoinCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_coin(db, coin_in)

@router.delete("/{coin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_coin(
    coin_id: int,
    db: AsyncSession = Depends(get_db)
):
    await delete_coin(db, coin_id)