import pandas as pd
import dask.dataframe as dd
from sqlalchemy import create_engine
from dask.distributed import Client

# Define the function to load data
def load_data(query: str, engine_conn):
    # Load the data into a Pandas DataFrame
    pandas_df = pd.read_sql_query(query, engine_conn)
    # Convert the Pandas DataFrame to a Dask DataFrame
    dask_df = dd.from_pandas(pandas_df, npartitions=10)
    return dask_df

# Main script
if __name__ == '__main__':
    # Create a Dask client
    client = Client()

    # Create the SQLAlchemy engine
    engine = create_engine('postgresql://postgres:RQaoNj7QEDxq@localhost:5433/Kemis_analytics_db')

    # Load data
    data = load_data("SELECT * FROM mv_market_summary_by_market_date_geo", engine)
    print(data.info())
