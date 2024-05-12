import psycopg2
from configparser import ConfigParser
import logging


def config(filename='db_config.ini', section='database_lake'):
    # Create a parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)

    # Get section, default to database
    db_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db_params

def connect(db_type="DataLake"):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        if db_type == "DataLake":
            # Read connection parameters
            params = config()
        elif db_type == "DataWarehouse":
            # Read connection parameters for database_warehouse
            params = config(section="database_warehouse")
        # Connect to the PostgreSQL server
        logging.info('------------ >  Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logging.info(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('------------ > Database connection closed. < ------------ ')
