-- These queries are based on PostgreSQL db

CREATE TABLE IF NOT EXISTS dim_commodity (
    id SERIAL PRIMARY KEY,
    commodity VARCHAR(50) NOT NULL
)

CREATE TABLE IF NOT EXISTS dim_market (
    id SERIAL PRIMARY KEY,
    market VARCHAR(100) NOT NULL
)

CREATE TABLE IF NOT EXISTS dim_grade (
    id SERIAL PRIMARY KEY,
    grade VARCHAR(50) NOT NULL
)

CREATE TABLE IF NOT EXISTS dim_sex (
    id SERIAL PRIMARY KEY,
    sex VARCHAR(10) NOT NULL
)

CREATE TABLE IF NOT EXISTS dim_county (
    id SERIAL PRIMARY KEY,
    county VARCHAR(50) NOT NULL
)

CREATE TABLE IF NOT EXISTS dim_date (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    quarter INT NOT NULL,
    week INT NOT NULL,
    fiscal_year INT NOT NULL
)

CREATE TABLE IF NOT EXISTS fact_market_prices (
    id SERIAL PRIMARY KEY,
    commodity_sk INT NOT NULL,
    grade_sk INT NOT NULL,
    sex_sk INT NOT NULL,
    market_sk INT NOT NULL,
    wholesale_price NUMERIC(10, 2) NOT NULL,
    retail_price NUMERIC(10, 2) NOT NULL,
    price_unit_wr VARCHAR(20) NOT NULL,
    supply_volume INT NOT NULL,
    county_sk INT NOT NULL,
    date_sk INT NOT NULL,
    FOREIGN KEY (commodity_sk) REFERENCES dim_commodity(id),
    FOREIGN KEY (market_sk) REFERENCES dim_market(id),
    FOREIGN KEY (grade_sk) REFERENCES dim_grade(id),
    FOREIGN KEY (sex_sk) REFERENCES dim_sex(id),
    FOREIGN KEY (date_sk) REFERENCES dim_date(id),
    FOREIGN KEY (county_sk) REFERENCES dim_county(id)
)

CREATE TABLE county_geo (
    id SERIAL PRIMARY KEY,
    county_sk INT NOT NULL,
    Address VARCHAR(255) NULL,
    Latitude DECIMAL(10, 8) NULL,
    Longitude DECIMAL(11, 8) NULL,
    FOREIGN KEY (county_sk) REFERENCES dim_county(id)
)

CREATE TABLE market_geo (
    id SERIAL PRIMARY KEY,
    market_sk INT NOT NULL,
    Address VARCHAR(300) NULL,
    Latitude DECIMAL(10, 8) NULL,
    Longitude DECIMAL(11, 8) NULL,
    FOREIGN KEY (market_sk) REFERENCES dim_market(id)
)

CREATE INDEX IF NOT EXISTS idx_fact_market_prices_date ON fact_market_prices (date_sk)

CREATE INDEX IF NOT EXISTS idx_fact_market_prices_county ON fact_market_prices (county_sk)
