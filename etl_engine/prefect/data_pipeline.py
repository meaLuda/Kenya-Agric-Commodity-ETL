import pandas as pd
from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner
from sqlalchemy import create_engine
from datetime import datetime

@task
def extract_data():
    source_db_url = "postgresql://postgres:RQaoNj7QEDxq@localhost:5432/kemis_data_db"
    source_engine = create_engine(source_db_url)
    
    target_db_url = "postgresql://postgres:RQaoNj7QEDxq@localhost:5432/kemis_analytics_db"
    target_engine = create_engine(target_db_url)
    
    # Get the latest date from the fact table in the analytics db
    latest_date_query = "SELECT MAX(date) FROM dim_date"
    latest_date = pd.read_sql(latest_date_query, target_engine).iloc[0, 0]
    
    if latest_date is None:
        query = "SELECT * FROM agriscrapper_data"
    else:
        query = f"SELECT * FROM agriscrapper_data WHERE date > '{latest_date}'"
    
    df = pd.read_sql(query, source_engine)
    return df

@task
def clean_data(df):
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Clean and convert prices
    for col in ['wholesale', 'retail']:
        df[col] = df[col].str.replace(' - ', '0')
        df[col] = df[col].str.extract('(\d+\.?\d*)').astype(float)
    
    # Convert supply_volume to numeric
    df['supply_volume'] = pd.to_numeric(df['supply_volume'], errors='coerce')
    
    # Fill NaN values
    df = df.fillna({
        'classification': 'Unknown',
        'grade': 'Unknown',
        'sex': 'Unknown',
        'wholesale': 0,
        'retail': 0,
        'supply_volume': 0
    })
    
    return df

@task
def transform_data(df):
    # Create dimension dataframes
    dim_commodity = df[['commodity']].drop_duplicates().reset_index(drop=True)
    dim_commodity['commodity_id'] = dim_commodity.index + 1
    
    dim_market = df[['market']].drop_duplicates().reset_index(drop=True)
    dim_market['market_id'] = dim_market.index + 1
    
    dim_grade = df[['grade']].drop_duplicates().reset_index(drop=True)
    dim_grade['grade_id'] = dim_grade.index + 1
    
    dim_sex = df[['sex']].drop_duplicates().reset_index(drop=True)
    dim_sex['sex_id'] = dim_sex.index + 1
    
    dim_county = df[['county']].drop_duplicates().reset_index(drop=True)
    dim_county['county_id'] = dim_county.index + 1
    
    dim_date = df[['date']].drop_duplicates().reset_index(drop=True)
    dim_date['date_id'] = dim_date.index + 1
    dim_date['year'] = dim_date['date'].dt.year
    dim_date['month'] = dim_date['date'].dt.month
    dim_date['day'] = dim_date['date'].dt.day
    dim_date['quarter'] = dim_date['date'].dt.quarter
    dim_date['week'] = dim_date['date'].dt.isocalendar().week
    dim_date['fiscal_year'] = dim_date['year']  # Assuming fiscal year is the same as calendar year
    
    # Create fact table
    fact_market_prices = df.merge(dim_commodity, on='commodity')
    fact_market_prices = fact_market_prices.merge(dim_market, on='market')
    fact_market_prices = fact_market_prices.merge(dim_grade, on='grade')
    fact_market_prices = fact_market_prices.merge(dim_sex, on='sex')
    fact_market_prices = fact_market_prices.merge(dim_county, on='county')
    fact_market_prices = fact_market_prices.merge(dim_date, on='date')
    
    fact_market_prices = fact_market_prices[[
        'commodity_id', 'classification', 'grade_id', 'sex_id', 'market_id',
        'wholesale', 'retail', 'supply_volume', 'county_id', 'date_id'
    ]]
    # Generate unique IDs for dimension tables
    for dim_table in [dim_commodity, dim_market, dim_grade, dim_sex, dim_county, dim_date]:
        dim_table[f'{dim_table.columns[0]}_id'] = range(1, len(dim_table) + 1)

    return {
        'dim_commodity': dim_commodity,
        'dim_market': dim_market,
        'dim_grade': dim_grade,
        'dim_sex': dim_sex,
        'dim_county': dim_county,
        'dim_date': dim_date,
        'fact_market_prices': fact_market_prices
    }

@task
def load_data(transformed_data):
    target_db_url = "postgresql://postgres:RQaoNj7QEDxq@localhost:5432/kemis_analytics_db"
    target_engine = create_engine(target_db_url)
    
    # Handle dimension tables
    for table_name in ['dim_commodity', 'dim_market', 'dim_grade', 'dim_sex', 'dim_county', 'dim_date']:
        df = transformed_data[table_name]
        existing_df = pd.read_sql(f"SELECT * FROM {table_name}", target_engine)
        
        # Identify new records
        merged = df.merge(existing_df, how='left', indicator=True)
        new_records = merged[merged['_merge'] == 'left_only'].drop('_merge', axis=1)
        
        if not new_records.empty:
            new_records.to_sql(table_name, target_engine, if_exists='append', index=False)
    
    # Handle fact table
    transformed_data['fact_market_prices'].to_sql('fact_market_prices', target_engine, if_exists='append', index=False)



@task
def deduplicate_fact_table():
    target_db_url = "postgresql://postgres:RQaoNj7QEDxq@localhost:5432/kemis_analytics_db"
    target_engine = create_engine(target_db_url)
    
    dedup_query = """
    DELETE FROM fact_market_prices
    WHERE id IN (
        SELECT id
        FROM (
            SELECT id,
                   ROW_NUMBER() OVER (
                       PARTITION BY commodity_id, market_id, grade_id, sex_id, county_id, date_id
                       ORDER BY id DESC
                   ) AS row_num
            FROM fact_market_prices
        ) t
        WHERE t.row_num > 1
    );
    """
    
    with target_engine.connect() as conn:
        conn.execute(dedup_query)


@flow(task_runner=SequentialTaskRunner())
def etl_flow():
    raw_data = extract_data()
    if not raw_data.empty:
        cleaned_data = clean_data(raw_data)
        transformed_data = transform_data(cleaned_data)
        load_data(transformed_data)
        deduplicate_fact_table()
    else:
        print("No new data to process.")

if __name__ == "__main__":
    etl_flow()