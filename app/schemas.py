from datetime import datetime
from pydantic import BaseModel, constr, condecimal
from typing import Optional, List

class CoinBase(BaseModel):
    cg_id: constr(min_length=1)
    symbol: constr(min_length=1, max_length=10)
    name: constr(min_length=1, max_length=100)

class CoinCreate(CoinBase):
    pass

class CoinResponse(CoinBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PriceRecordBase(BaseModel):
    recorded_at: datetime
    price_usd: condecimal(max_digits=18, decimal_places=8)
    volume_24h: Optional[condecimal(max_digits=20, decimal_places=2)]
    price_change_24h: Optional[condecimal(max_digits=6, decimal_places=2)]

class PriceRecordResponse(PriceRecordBase):
    class Config:
        orm_mode = True

class PriceListResponse(BaseModel):
    count: int
    list: List[PriceRecordResponse]