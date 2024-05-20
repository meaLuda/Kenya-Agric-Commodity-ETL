import psycopg2
from configparser import ConfigParser
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the base directory as the directory where the main script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path to the configuration file
config_file_path = os.path.join(BASE_DIR, 'db_config.ini')


def config(filename=config_file_path, section='database_lake'):
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
        logging.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        logging.info('Connection successful')

        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error('Connection failed')
        logging.error(error)
        return None


def create_tables():
    """ Create tables in the PostgreSQL database """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS dim_commodity (
            id SERIAL PRIMARY KEY,
            commodity_name VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS dim_market (
            id SERIAL PRIMARY KEY,
            market_name VARCHAR(100) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS dim_grade (
            id SERIAL PRIMARY KEY,
            grade_name VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS dim_sex (
            id SERIAL PRIMARY KEY,
            sex_name VARCHAR(10) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS dim_county (
            id SERIAL PRIMARY KEY,
            county_name VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS dim_date (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            year INT NOT NULL,
            month INT NOT NULL,
            day INT NOT NULL,
            quarter INT NOT NULL,
            week INT NOT NULL,
            fiscal_year INT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS fact_market_prices (
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
            FOREIGN KEY (commodity_sk) REFERENCES dim_commodity(id),
            FOREIGN KEY (market_sk) REFERENCES dim_market(id),
            FOREIGN KEY (grade_sk) REFERENCES dim_grade(id),
            FOREIGN KEY (sex_sk) REFERENCES dim_sex(id),
            FOREIGN KEY (date_sk) REFERENCES dim_date(id),
            FOREIGN KEY (county_sk) REFERENCES dim_county(id)
        )
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_fact_market_prices_date ON fact_market_prices (date_sk)
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_fact_market_prices_county ON fact_market_prices (county_sk)
        """
    )

    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = connect("DataWarehouse")
        if conn is None:
            raise Exception("Connection to the database failed")

        cur = conn.cursor()
        # Execute each command
        for command in commands:
            cur.execute(command)
            logging.info(f"Executed: {command}")

        # Close communication with the database
        cur.close()
        # Commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


# Example usage
# if __name__ == '__main__':
#     conn = connect()
#     print(conn)
#     if conn is not None:
#         logging.info('Connection object: %s', conn)
#         conn.close()
