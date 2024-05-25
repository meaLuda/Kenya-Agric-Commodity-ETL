import pandas as pd
from sqlalchemy import create_engine
from db.db_conn import config
import sys
import logging

def extract_data():
    # Define options for reading data
    table_name = "agriscrapper_data"
    query_condition = "commodity='Dry Maize' AND wholesale!=' - ' AND retail!=' - ' AND supply_volume!=''"

    try:
        logging.info("loading data from database")
        # Get the connection string from the config
        params = config()
        connection_string = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}"

        # Create a SQLAlchemy engine
        engine = create_engine(connection_string)
        connection = engine.raw_connection()
        cursor = connection.cursor()

        # Execute the query and fetch all rows
        cursor.execute(f"SELECT * FROM {table_name} WHERE {query_condition}")
        rows = cursor.fetchall()

        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Yield each row as a dictionary
        for row in rows:
            yield dict(zip(column_names, row))
    except Exception as e:
        import traceback
        logging.error("Error reading data from the database: %s", e)
        logging.error(traceback.format_exc())
        sys.exit(1)
    finally:
        # Close the database connection
        cursor.close()
        connection.close()
