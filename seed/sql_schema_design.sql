
-- The fact_market_prices table is the central fact table, containing the numerical measures
-- (wholesale price, retail price, supply volume) and foreign key references to the dimension tables.
-- The dimension tables (dim_commodity, dim_market, dim_grade, dim_sex, dim_county, dim_date)
-- store the descriptive attributes related to the fact data.
-- This design allows for efficient querying and filtering based on the dimensions,
-- as well as performing aggregations and analytical operations on the numerical measures in the fact table.



-- Dimensions table
-- Commodity Dimension
CREATE TABLE dim_commodity (
    commodity_sk SERIAL PRIMARY KEY,
    commodity_name VARCHAR(50) NOT NULL
);

-- Market Dimension
CREATE TABLE dim_market (
    market_sk SERIAL PRIMARY KEY,
    market_name VARCHAR(100) NOT NULL
);

-- Grade Dimension
CREATE TABLE dim_grade (
    grade_sk SERIAL PRIMARY KEY,
    grade_name VARCHAR(50) NOT NULL
);

-- Sex Dimension
CREATE TABLE dim_sex (
    sex_sk SERIAL PRIMARY KEY,
    sex_name VARCHAR(10) NOT NULL
);

-- County Dimension
CREATE TABLE dim_county (
    county_sk SERIAL PRIMARY KEY,
    county_name VARCHAR(50) NOT NULL
);

-- Date Dimension
CREATE TABLE dim_date (
    date_sk SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL,
    quarter INT NOT NULL,
    week INT NOT NULL,
    fiscal_year INT NOT NULL
);

-- Fact Table
CREATE TABLE fact_market_prices (
    id SERIAL PRIMARY KEY,
    commodity_sk INT NOT NULL,
    grade_sk INT NOT NULL,
    sex_sk INT NOT NULL,
    market_sk INT NOT NULL,
    wholesale_price NUMERIC(10, 2) NOT NULL,
    retail_price NUMERIC(10, 2) NOT NULL,
    supply_volume INT NOT NULL,
    county_sk INT NOT NULL,
    date_sk INT NOT NULL,
    FOREIGN KEY (commodity_sk) REFERENCES dim_commodity(commodity_sk),
    FOREIGN KEY (market_sk) REFERENCES dim_market(market_sk),
    FOREIGN KEY (grade_sk) REFERENCES dim_grade(grade_sk),
    FOREIGN KEY (sex_sk) REFERENCES dim_sex(sex_sk),
    FOREIGN KEY (date_sk) REFERENCES dim_date(date_sk),
    FOREIGN KEY (county_sk) REFERENCES dim_county(county_sk)
);

-- Indexes (example)
CREATE INDEX idx_fact_market_prices_date ON fact_market_prices (date_sk);
CREATE INDEX idx_fact_market_prices_county ON fact_market_prices (county_sk);
