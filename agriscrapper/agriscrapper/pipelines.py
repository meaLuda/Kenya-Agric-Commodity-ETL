from itemadapter import ItemAdapter
from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import os
from os.path import join, dirname
import logging

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

logging.basicConfig(filename='AgriscrapperPipeline_to_db.log', level=logging.INFO)

DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

class AgriscrapperPipeline:
    def __init__(self):
        hostname = DB_HOST
        username = 'postgres'
        password = DB_PASSWORD
        port = DB_PORT
        database = 'kemis_data_db'

        if not all([hostname, username, password, port, database]):
            raise ValueError("Missing database connection details. Please check your environment variables.")

        # Create the SQLAlchemy engine
        self.engine = create_engine(f'postgresql+pg8000://{username}:{password}@{hostname}:{port}/{database}')
        
        # Create a metadata instance
        self.metadata = MetaData()

        # Define the table
        self.agriscrapper_data = Table('agriscrapper_data', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('commodity', String),
            Column('classification', String),
            Column('grade', String),
            Column('sex', String),
            Column('market', String),
            Column('wholesale', String),
            Column('retail', String),
            Column('supply_volume', String),
            Column('county', String),
            Column('date', String)
        )

        # Create the table if it doesn't exist
        self.metadata.create_all(self.engine)

        # Create a session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def process_item(self, item, spider):
        try:
            # Check if the entry already exists
            existing_entry = self.session.query(self.agriscrapper_data).filter_by(
                commodity=item["commodity"],
                classification=item["classification"],
                grade=item["grade"],
                sex=item["sex"],
                market=item["market"],
                wholesale=item["wholesale"],
                retail=item["retail"],
                supply_volume=item["supply_volume"],
                county=item["county"],
                date=item["date"]
            ).first()

            if existing_entry is None:
                # Entry does not exist, insert new data
                new_entry = self.agriscrapper_data.insert().values(**item)
                self.session.execute(new_entry)
                self.session.commit()
                logging.info(f"Inserted new entry: {item['commodity']}")
            else:
                logging.info(f"Entry already exists. Skipping insertion: {item['commodity']}")

        except IntegrityError:
            self.session.rollback()
            logging.error(f"IntegrityError: Failed to insert {item['commodity']}")
        except Exception as e:
            self.session.rollback()
            logging.error(f"Error processing item: {str(e)}")

        return item

    def close_spider(self, spider):
        # Close the session
        self.session.close()