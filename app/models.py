from sqlalchemy import (
    Column, Integer, BigInteger, Numeric, String, TIMESTAMP,
    func, UniqueConstraint, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Coin(Base):
    __tablename__ = 'coin'  # Имя таблицы в БД (singular)
    id = Column(Integer, primary_key=True, index=True)
    cg_id = Column(String(64), unique=True, nullable=False, index=True)
    symbol = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

class PriceRecord(Base):
    __tablename__ = 'price_records'
    id = Column(BigInteger, primary_key=True, index=True)
    coin_id = Column(Integer, ForeignKey('coin.id', ondelete='CASCADE'), nullable=False, index=True)
    recorded_at = Column(TIMESTAMP(timezone=True), nullable=False)
    price_usd = Column(Numeric(18,8), nullable=False)
    volume_24h = Column(Numeric(20,2), nullable=True)
    price_change_24h = Column(Numeric(6,2), nullable=True)
    __table_args__ = (
        UniqueConstraint('coin_id', 'recorded_at', name='uix_coin_time'),
    )