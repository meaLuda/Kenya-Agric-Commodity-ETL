import pandas as pd
import psycopg2
import re
from datetime import datetime

def load_data_into_tables(data_file, conn):
    # Read the data from the file into a pandas DataFrame
    df = pd.read_csv(data_file)

    # Convert date column to datetime format
    try:
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
    except ValueError:
        print("Error: Invalid date format in the data file. Expected format is 'dd/mm/yyyy'.")
        return

    # Handle null values
    df = df.fillna(0)

    # Convert numeric columns to appropriate data types and extract units
    df['wholesale'], df['wholesale_unit'] = df['wholesale'].apply(extract_value_and_unit).str
    df['retail'], df['retail_unit'] = df['retail'].apply(extract_value_and_unit).str
    df['supply_volume'] = df['supply_volume'].apply(lambda x: int(x) if x != 0 else 0)
    df['unit'] = df[['wholesale_unit', 'retail_unit']].fillna('No Unit').mode(axis=1)[0]

    # Create separate DataFrames for each dimension table
    dim_commodity = pd.DataFrame({'commodity_name': df['commodity'].unique()})
    dim_market = pd.DataFrame({'market_name': df['market'].unique()})
    dim_grade = pd.DataFrame({'grade_name': df['grade'].unique()})
    dim_sex = pd.DataFrame({'sex_name': df['sex'].unique()})
    dim_county = pd.DataFrame({'county_name': df['county'].unique()})
    dim_date = pd.DataFrame({
        'date': df['date'].unique(),
        'year': df['date'].dt.year,
        'month': df['date'].dt.month,
        'day': df['date'].dt.day,
        'quarter': df['date'].dt.quarter,
        'week': df['date'].dt.isocalendar().week,
        'fiscal_year': df['date'].dt.year  # Assuming fiscal year is the same as calendar year
    })

    # Insert data into dimension tables
    insert_dim_table(conn, dim_commodity, 'dim_commodity', 'commodity_name')
    insert_dim_table(conn, dim_market, 'dim_market', 'market_name')
    insert_dim_table(conn, dim_grade, 'dim_grade', 'grade_name')
    insert_dim_table(conn, dim_sex, 'dim_sex', 'sex_name')
    insert_dim_table(conn, dim_county, 'dim_county', 'county_name')
    insert_dim_table(conn, dim_date, 'dim_date', ['date', 'year', 'month', 'day', 'quarter', 'week', 'fiscal_year'])

    # Insert data into the fact table
    insert_fact_table(conn, df)

def extract_value_and_unit(value):
    """
        uses regular expressions to extract the numeric value and the unit of measurement from the wholesale and retail columns.
        regular expression pattern r"(\d+(\.\d+)?)\s*(/?\w+)?" matches a numeric value followed by an optional unit. 
        It captures the numeric value and the unit (if present) as separate groups.
        If no unit is provided, the default unit 'No Unit' is used.
    """
    if isinstance(value, str):
        pattern = r"(\d+(\.\d+)?)\s*(/?\w+)?"
        match = re.match(pattern, value)
        if match:
            value_str, unit = match.groups()
            return float(value_str), unit.strip('/') if unit else 'No Unit'
    return value, 'No Unit'

def insert_dim_table(conn, df, table_name, columns):
    cursor = conn.cursor()

    # Insert data into the dimension table
    for _, row in df.iterrows():
        values = [row[col] for col in columns]
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        cursor.execute(query, values)

    conn.commit()
    cursor.close()

def insert_fact_table(conn, df):
    cursor = conn.cursor()

    # Insert data into the fact table
    for _, row in df.iterrows():
        # Skip rows with null values when inserting into the fact table
        if pd.isna(row['wholesale']) or pd.isna(row['retail']) or pd.isna(row['supply_volume']):
            continue
        commodity_id = get_id(conn, 'dim_commodity', 'commodity_name', row['commodity'])
        market_id = get_id(conn, 'dim_market', 'market_name', row['market'])
        grade_id = get_id(conn, 'dim_grade', 'grade_name', row['grade'])
        sex_id = get_id(conn, 'dim_sex', 'sex_name', row['sex'])
        county_id = get_id(conn, 'dim_county', 'county_name', row['county'])
        date_id = get_id(conn, 'dim_date', ['date', 'year', 'month', 'day', 'quarter', 'week', 'fiscal_year'],
                         [row['date'], row['date'].year, row['date'].month, row['date'].day,
                          row['date'].quarter, row['date'].isocalendar().week, row['date'].year])

        values = [commodity_id, market_id, grade_id, sex_id, row['wholesale'], row['retail'],
                  row['supply_volume'], date_id, county_id, row['unit']]
        placeholders = ', '.join(['%s'] * len(values))
        query = f"INSERT INTO fact_market_prices (commodity_id, market_id, grade_id, sex_id, wholesale_price, retail_price, supply_volume, date_id, county_id, unit) VALUES ({placeholders})"
        cursor.execute(query, values)

    conn.commit()
    cursor.close()

def get_id(conn, table_name, column_name, value):
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

# Example usage
conn = psycopg2.connect("dbname=your_database user=your_user password=your_password")
load_data_into_tables('data.csv', conn)
conn.close()