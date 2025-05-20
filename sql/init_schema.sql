-- 1. Таблица монет
CREATE TABLE coins (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    cg_id VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Таблица ценовых записей
CREATE TABLE price_records (
    id SERIAL PRIMARY KEY,
    coin_id INTEGER REFERENCES coins(id),
    price_usd DECIMAL(20, 8) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Индексы
CREATE INDEX idx_price_records_coin_id ON price_records(coin_id);
CREATE INDEX idx_price_records_timestamp ON price_records(timestamp);
