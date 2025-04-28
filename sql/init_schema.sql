-- 1. Таблица монет
CREATE TABLE coin (
  id         SERIAL PRIMARY KEY,
  cg_id      VARCHAR(64) NOT NULL UNIQUE,
  symbol     VARCHAR(10) NOT NULL,
  name       VARCHAR(100) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 2. Таблица ценовых записей
CREATE TABLE price_records (
  id                   BIGSERIAL PRIMARY KEY,
  coin_id             INTEGER NOT NULL REFERENCES coin(id) ON DELETE CASCADE,
  recorded_at          TIMESTAMPTZ NOT NULL,
  price_usd            NUMERIC(18,8) NOT NULL,
  volume_24h           NUMERIC(20,2),
  price_change_24h     NUMERIC(6,2),
  UNIQUE (coin_id, recorded_at)
);

-- 3. Индексы
CREATE INDEX idx_price_coin_time
  ON price_records(coin_id, recorded_at DESC);



