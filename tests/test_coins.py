import pytest
from app.schemas import CoinCreate

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