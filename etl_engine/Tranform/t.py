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
    data['wholesale'], wholesale_unit = zip(*data['wholesale'].apply(lambda x: extract_value_and_unit(x)))
    data['retail'], retail_unit = zip(*data['retail'].apply(lambda x: extract_value_and_unit(x)))
    data['supply_volume'] = data['supply_volume'].astype(float)
    data['retail'] = data['retail'].astype(float)
    data['wholesale'] = data['wholesale'].astype(float)
    if wholesale_unit == retail_unit:
        data['price_unit_wr'] = wholesale_unit


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
    insert_dim_table(conn, dim_commodity, 'dim_commodity', ['commodity'])
    insert_dim_table(conn, dim_market, 'dim_market',['market'])
    insert_dim_table(conn, dim_grade, 'dim_grade', ['grade'])
    insert_dim_table(conn, dim_sex, 'dim_sex', ['sex'])
    insert_dim_table(conn, dim_county, 'dim_county', ['county'])
    insert_dim_table(conn, dim_date, 'dim_date', ['date', 'year', 'month', 'day', 'quarter', 'week', 'fiscal_year'])

    ## Insert data into the fact table
    insert_fact_table(conn, data)


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

def insert_dim_table(conn, df, table_name, columns_df):
    logging.info(f"------------ Inserting into {table_name} Table  --------------------------")

    cursor = conn.cursor()
    logging.info(df)
    print("\n")

    ## Convert DataFrame values to a list of tuples
    values = [tuple(row) for row in df.values.tolist()]

    ## Create the query with placeholders for each row
    placeholders = ', '.join(['%s'] * len(columns_df))
    query = f"INSERT INTO {table_name} ({', '.join(columns_df)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"

    ## Execute the insert query for each row of values
    for value in values:
        cursor.execute(query, value)

    conn.commit()
    cursor.close()


def insert_fact_table(conn, df):
    logging.info("------------ Inserting into Fact Table  --------------------------")

    # Create a list to store the tuples of values for insertion
    rows_to_insert = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        commodity_sk = get_id(conn, 'dim_commodity', 'commodity', row['commodity'])
        market_sk = get_id(conn, 'dim_market', 'market', row['market'])
        grade_sk = get_id(conn, 'dim_grade', 'grade', row['grade'])
        sex_sk = get_id(conn, 'dim_sex', 'sex', row['sex'])
        county_sk = get_id(conn, 'dim_county', 'county', row['county'])

        date_sk = get_id(conn, 'dim_date',
            ['date', 'year', 'month', 'day', 'quarter', 'week', 'fiscal_year'],
            row[['date', 'year', 'month', 'day', 'quarter', 'week', 'fiscal_year']].tolist()
            )

        values = (commodity_sk, grade_sk, sex_sk, market_sk, row['wholesale'], row['retail'],row['price_unit_wr'],
            row['supply_volume'], county_sk, date_sk)

        rows_to_insert.append(values)

    placeholders = ', '.join(['%s'] * len(rows_to_insert[0]))
    query = f"INSERT INTO fact_market_prices (commodity_sk, grade_sk, sex_sk, market_sk, wholesale_price, retail_price,price_unit_wr, supply_volume, county_sk, date_sk) VALUES ({placeholders})"

    cursor = conn.cursor()

    # Execute the insert query for each row of values
    for values in rows_to_insert:
        cursor.execute(query, values)

    conn.commit()
    cursor.close()
