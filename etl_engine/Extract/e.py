import dask.dataframe as dd
from db.db_conn import connect
import sys
import logging


def extract_data():
    try:
        conn = connect(db_type="DataWarehouse")
    except Exception as e:
        logging.error("Error connecting to the database:", e)
        sys.exit(1)

    # Define options for reading data
    table_name = "agriscrapper_data"
    column_selection = "*"
    query_condition = "commodity='Dry Maize' AND wholesale!=' - ' AND retail!=' - ' AND supply_volume!=''"

    try:
        logging.info("loading data from database")
        # Read data in chunks directly from the database using Dask
        df = dd.read_sql_table(table_name, conn, index_col='index', divisions=True, npartitions=4,
                               columns=column_selection, where=query_condition)
    except Exception as e:
        logging.error("Error reading data from the database:", e)
        sys.exit(1)

    return df
