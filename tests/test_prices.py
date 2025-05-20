import pytest
from datetime import datetime, timedelta
from app.schemas import PriceRecordResponse
from app.models import Coin, PriceRecord
from app.crud import create_coin, get_latest_price
from app.crawler import fetch_and_store

@pytest.mark.asyncio
async def test_price_flow(client):

    await client.post('/api/v1/coins/', json={'cg_id':'testcoin','symbol':'tst','name':'Test'})
    coins = await client.get('/api/v1/coins/')
    coin_id = coins.json()[0]['id']
    
    await fetch_and_store.__wrapped__( 
        db=client.app.dependency_overrides[get_db](),
        cg_id='testcoin', coin_id=coin_id
    )

    
    resp = await client.get(f'/api/v1/coins/{coin_id}/prices/latest')
    assert resp.status_code == 200
    pr = PriceRecordResponse(**resp.json())
    assert pr.price_usd >= 0

@pytest.mark.asyncio
async def test_price_records(db_session):
    coin = await create_coin(db_session, "BTC", "Bitcoin")
    await fetch_and_store.__wrapped__()
    latest = await get_latest_price(db_session, coin.id)
    assert latest is not None
    assert latest.price > 0