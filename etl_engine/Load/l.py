import pandas as pd
from sqlalchemy import create_engine
from db.db_conn import config
import sys
import logging

def load_data_into_db(df):
    try:
        logging.info("connecting to the database")
        # Get the connection string from the config
        params = config()
        connection_string = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['dbname']}"

        # Create a SQLAlchemy engine
        engine = create_engine(connection_string)

        # Write DataFrame to SQL table
        df.to_sql('Kemis_analytics_db', engine, if_exists='append', index=False)  # Adjust target table name

        logging.info("data loaded into the database successfully")
    except Exception as e:
        import traceback
        logging.error("Error loading data into the database: %s", e)
        logging.error(traceback.format_exc())
        sys.exit(1)


logging.info("load etl")
