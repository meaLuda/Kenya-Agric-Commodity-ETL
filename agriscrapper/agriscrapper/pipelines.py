# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from dotenv import load_dotenv
import os
import os
from os.path import join, dirname
from dotenv import load_dotenv
import logging


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# logg into a file
# logging.basicConfig(filename='AgriscrapperPipeline_to_db.log', level=logging.INFO)

DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PORT = os.environ.get("DATABASE_PORT")



class AgriscrapperPipeline:
    def __init__(self):
        ## Connection Details
        hostname = DATABASE_HOST
        username = DATABASE_USER
        password = DATABASE_PASSWORD
        database = DATABASE_NAME

        ## Create/Connect to database
        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.connection.autocommit = True  # Set autocommit mode
        self.cur = self.connection.cursor()

        # Check if the database exists, and create it if it doesn't
        self.cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (database,))
        if not self.cur.fetchone():
            self.cur.execute(f'CREATE DATABASE {database}')

        # Now connect to the newly created database
        self.connection.close()
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS agriscrapper_data (
            id SERIAL PRIMARY KEY,
            commodity TEXT NULL,
            classification TEXT NULL,
            grade TEXT NULL,
            sex TEXT NULL,
            market TEXT NULL,
            wholesale TEXT NULL,
            retail TEXT NULL,
            supply_volume TEXT NULL,
            county TEXT NULL,
            date TEXT NULL
        );
        """)
    
    def process_item(self, item, spider):
        # Define the select statement to check for existing entry
        # This prevents double entry from being created by our scraper
        select_statement = """
            SELECT id FROM agriscrapper_data
            WHERE commodity = %s AND classification = %s AND grade = %s AND sex = %s
                AND market = %s AND wholesale = %s AND retail = %s AND supply_volume = %s
                AND county = %s AND date = %s
        """

        # Execute the select statement with item data
        self.cur.execute(select_statement, (
            item["commodity"],
            item["classification"],
            item["grade"],
            item["sex"],
            item["market"],
            item["wholesale"],
            item["retail"],
            item["supply_volume"],
            item["county"],
            item["date"]
        ))

        # Fetch the result of the SELECT query
        existing_entry = self.cur.fetchone()

        # Check if the entry already exists
        if existing_entry is None:
            # Entry does not exist, proceed with the insert statement
            insert_statement = """
                INSERT INTO agriscrapper_data
                (commodity, classification, grade, sex, market, wholesale, retail, supply_volume, county, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Execute the insert statement with item data
            self.cur.execute(insert_statement, (
                item["commodity"],
                item["classification"],
                item["grade"],
                item["sex"],
                item["market"],
                item["wholesale"],
                item["retail"],
                item["supply_volume"],
                item["county"],
                item["date"]
            ))

            # Commit the changes to the database
            self.connection.commit()
        else:
            ("Entry already exists. Skipping insertion.")

        return item

    def close_spider(self, spider):
        # Close the cursor and connection
        self.cur.close()
        self.connection.close()

