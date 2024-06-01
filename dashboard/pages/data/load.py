import pandas as pd
from sqlalchemy import create_engine

# Define the function to load data
def load_data(query: str):
    # Create the SQLAlchemy engine
    engine = create_engine('postgresql://postgres:RQaoNj7QEDxq@localhost:5433/Kemis_analytics_db')
    # Load the data into a Pandas DataFrame
    pandas_df = pd.read_sql_query(query, engine)

    return pandas_df
