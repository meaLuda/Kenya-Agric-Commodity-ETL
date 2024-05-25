import pandas as pd
import logging
from db.db_conn import connect,create_tables
from Extract.e import extract_data
from Tranform.t import transform_data_into_tables

if __name__ == "__main__":
    ## create tables
    # try:
    #     create_tables()
    # except Exception as e:
    #     logging.info(e)
    count = 0
    for row in extract_data():
        conn = connect("DataWarehouse")
        transform_data_into_tables(row,conn)
        # count += 1
        # if count == 2:
        #     break
