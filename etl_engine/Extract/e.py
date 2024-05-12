import dask.dataframe as dd
import pandas as pd
from db.db_conn import connect

def extract_data():
    conn = connect(db_type="DataWarehouse")

    # -------- load fitler
    df = dd.from_pandas(pd.read_sql_query("""SELECT * FROM agriscrapper_data\
    WHERE commodity='Dry Maize' AND wholesale!=' - '\
    AND retail!=' - 'AND supply_volume!='';""", conn), npartitions=4)

    # return extracted data as dask dataframe with 4 partitions from data lake
    return df
