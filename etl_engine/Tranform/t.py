import pandas as pd
import logging
from datetime import datetime


def get_id(conn, table_name, column_name, value):
    logging.info("------------ Getting ID  --------------------------")

    cursor = conn.cursor()
    if isinstance(column_name, list):
        placeholders = ', '.join(['%s'] * len(column_name))
        query = f"SELECT id FROM {table_name} WHERE ({', '.join(column_name)}) = ({placeholders})"
        cursor.execute(query, value)
    else:
        query = f"SELECT id FROM {table_name} WHERE {column_name} = %s"
        cursor.execute(query, (value,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None


def transform_data_into_tables(data, conn):
    data = pd.DataFrame.from_dict([data])
    # Convert date column to datetime format
    try:
        data['date'] = pd.to_datetime(data['date'])
    except ValueError:
        logging.info("Error: Invalid date format in the data file. Expected format is 'dd/mm/yyyy'.")
        return

    # Convert numeric columns to appropriate data types and extract units
    data['wholesale'], data['wholesale_unit'] = zip(*data['wholesale'].apply(lambda x: extract_value_and_unit(x)))
    data['retail'], data['retail_unit'] = zip(*data['retail'].apply(lambda x: extract_value_and_unit(x)))
    data['supply_volume'] = data['supply_volume'].astype(float)
    data['retail'] = data['retail'].astype(float)
    data['wholesale'] = data['wholesale'].astype(float)


    # # Create separate DataFrames for each dimension table
    dim_commodity = data[['commodity']]
    dim_market =  data[['market']]
    dim_grade = data[['grade']]
    dim_sex =  data[['sex']]
    dim_county =  data[['county']]

    # Extract unique dates and create the date dimension table
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data['day'] = data['date'].dt.day
    data['quarter'] = data['date'].dt.quarter
    data['week'] = data['date'].dt.isocalendar().week
    data['fiscal_year'] = data['date'].dt.year  # Assuming fiscal year is the same as calendar year
    dim_date = data[['date', 'year', 'month', 'day', 'quarter', 'week', 'fiscal_year']]
    ## Insert data into dimension tables
    insert_dim_table(conn, dim_commodity, 'dim_commodity', ['commodity'], ['commodity_name'])
    # insert_dim_table(conn, dim_market, 'dim_market',['market'])
    # insert_dim_table(conn, dim_grade, 'dim_grade', ['grade_name'])
    # insert_dim_table(conn, dim_sex, 'dim_sex', ['sex_name'])
    # insert_dim_table(conn, dim_county, 'dim_county', ['county_name'])
    # insert_dim_table(conn, dim_date, 'dim_date', ['date', 'year', 'month', 'day', 'quarter', 'week', 'fiscal_year'], ['date', 'year', 'month', 'day', 'quarter', 'week', 'fiscal_year'])

    ## Insert data into the fact table
    insert_fact_table(conn, data)

    # return data

def extract_value_and_unit(value):
    """
    Splits the input string on the '/' character to extract the value and unit.
    If no '/' is present, the entire string is treated as the value, and 'No Unit' is used as the unit.
    """
    if isinstance(value, str):
        parts = value.split('/')
        print(parts)
        if len(parts) > 1:
            value_str, unit = parts
            return value_str, unit.strip()
        else:
            return value, 'No Unit'
    else:
        return value, 'No Unit'

def insert_dim_table(conn, df, table_name, columns_df,columns_pg):
    logging.info(f"------------ Inserting into {table_name} Table  --------------------------")

    cursor = conn.cursor()
    logging.info(df)
    ## Insert data into the dimension table
    for _, row in df.iterrows():
        values = [row[col] for col in columns_df]
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} ({', '.join(columns_pg)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        cursor.execute(query, values)

    conn.commit()
    cursor.close()

def insert_fact_table(conn, df):
    logging.info("------------ Inserting into Fact Table  --------------------------")

    cursor = conn.cursor()

    # Insert data into the fact table
    for _, row in df.iterrows():
        # Skip rows with null values when inserting into the fact table
        if pd.isna(row['wholesale']) or pd.isna(row['retail']) or pd.isna(row['supply_volume']):
            continue
        commodity_id = get_id(conn, 'dim_commodity', 'commodity_name', row['commodity'])
        logging.info(commodity_id)

        # market_id = get_id(conn, 'dim_market', 'market_name', row['market'])
        # grade_id = get_id(conn, 'dim_grade', 'grade_name', row['grade'])
        # sex_id = get_id(conn, 'dim_sex', 'sex_name', row['sex'])
        # county_id = get_id(conn, 'dim_county', 'county_name', row['county'])
        # date_id = get_id(conn, 'dim_date', ['date', 'year', 'month', 'day', 'quarter', 'week', 'fiscal_year'],
        #                  [row['date'], row['date'].year, row['date'].month, row['date'].day,
        #                   row['date'].quarter, row['date'].isocalendar().week, row['date'].year])

        # values = [commodity_id, market_id, grade_id, sex_id, row['wholesale'], row['retail'],
        #           row['supply_volume'], date_id, county_id, row['unit']]
        # placeholders = ', '.join(['%s'] * len(values))
        # query = f"INSERT INTO fact_market_prices (commodity_id, market_id, grade_id, sex_id, wholesale_price, retail_price, supply_volume, date_id, county_id, unit) VALUES ({placeholders})"

    #     cursor.execute(query, values)

    # conn.commit()
    cursor.close()

print("hello")
