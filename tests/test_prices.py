import pytest
from datetime import datetime, timedelta
from app.schemas import PriceRecordResponse

@pytest.mark.asyncio
async def test_price_flow(client):
    # Добавляем монету
    await client.post('/api/v1/coins/', json={'cg_id':'testcoin','symbol':'tst','name':'Test'})
    coins = await client.get('/api/v1/coins/')
    coin_id = coins.json()[0]['id']

    # Симулируем запись цены напрямую в БД через API (или прямым CRUD)
    # Для интеграции: используем crawler для одного прохода
    from app.crawler.crawler import fetch_and_store
    # Этот импорт и вызов допустимы в тестовом контексте
    await fetch_and_store.__wrapped__( # обход декораторов get_db
        db=client.app.dependency_overrides[get_db](),
        cg_id='testcoin', coin_id=coin_id
    )

    # Проверяем latest
    resp = await client.get(f'/api/v1/coins/{coin_id}/prices/latest')
    assert resp.status_code == 200
    pr = PriceRecordResponse(**resp.json())
    assert pr.price_usd >= 0