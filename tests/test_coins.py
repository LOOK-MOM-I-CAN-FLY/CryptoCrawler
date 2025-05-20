import pytest
from app.schemas import CoinCreate
from app.models import Coin
from app.crud import create_coin, get_coins

@pytest.mark.asyncio
async def test_create_and_list_coins(client):
    # Создание
    payload = CoinCreate(cg_id='bitcoin', symbol='btc', name='Bitcoin').dict()
    resp = await client.post('/api/v1/coins/', json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data['cg_id'] == 'bitcoin'
    # Список
    resp = await client.get('/api/v1/coins/')
    assert resp.status_code == 200
    lst = resp.json()
    assert any(c['cg_id']=='bitcoin' for c in lst)

async def test_create_coin(db_session):
    coin = await create_coin(db_session, "BTC", "Bitcoin")
    assert coin.symbol == "BTC"
    assert coin.name == "Bitcoin"

async def test_get_coins(db_session):
    await create_coin(db_session, "BTC", "Bitcoin")
    await create_coin(db_session, "ETH", "Ethereum")
    coins = await get_coins(db_session)
    assert len(coins) == 2