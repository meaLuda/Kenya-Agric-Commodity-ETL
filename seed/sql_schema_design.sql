
-- The fact_market_prices table is the central fact table, containing the numerical measures 
-- (wholesale price, retail price, supply volume) and foreign key references to the dimension tables.
-- The dimension tables (dim_commodity, dim_market, dim_grade, dim_sex, dim_county, dim_date) 
-- store the descriptive attributes related to the fact data.
-- This design allows for efficient querying and filtering based on the dimensions, 
-- as well as performing aggregations and analytical operations on the numerical measures in the fact table.

-- Dimensions table

-- Commodity Dimension
CREATE TABLE dim_commodity (
    commodity_id SERIAL PRIMARY KEY,
    commodity_name VARCHAR(50)
);

-- Market Dimension
CREATE TABLE dim_market (
    market_id SERIAL PRIMARY KEY,
    market_name VARCHAR(100)
);

-- Grade Dimension
CREATE TABLE dim_grade (
    grade_id SERIAL PRIMARY KEY,
    grade_name VARCHAR(50)
);

-- Sex Dimension
CREATE TABLE dim_sex (
    sex_id SERIAL PRIMARY KEY,
    sex_name VARCHAR(10)
);

-- County Dimension
CREATE TABLE dim_county (
    county_id SERIAL PRIMARY KEY,
    county_name VARCHAR(50)
);

-- Date Dimension
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    date DATE,
    year INT,
    month INT,
    day INT,
    quarter INT,
    week INT,
    fiscal_year INT
);

-- Fact Table
CREATE TABLE fact_market_prices (
    id SERIAL PRIMARY KEY,
    commodity_id INT,
    classification VARCHAR(50),
    grade_id INT,
    sex_id INT,
    market_id INT,
    wholesale_price DECIMAL(10, 2),
    wholesale_unit VARCHAR(50),
    retail_price DECIMAL(10, 2),
    retail_unit VARCHAR(50),
    supply_volume INT,
    county_id INT,
    date_id INT,
    FOREIGN KEY (commodity_id) REFERENCES dim_commodity(commodity_id),
    FOREIGN KEY (market_id) REFERENCES dim_market(market_id),
    FOREIGN KEY (grade_id) REFERENCES dim_grade(grade_id),
    FOREIGN KEY (sex_id) REFERENCES dim_sex(sex_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (county_id) REFERENCES dim_county(county_id)
);
