import pandas as pd
from db.db_conn import connect,create_tables
from Extract.e import extract_data
from Tranform.t import transform_data_into_tables

# ----------Create analytics table
# create_tables()

# ddf = extract_data()

# new_frame = ddf.iloc[:1].copy()
# # print(ddf.head())
# # print(new_frame.head())
# df = transform_data_into_tables(new_frame)
# print(df.head(20))
# print(df.isnull().sum())
# df.to_csv("test.csv")

count = 0
for row in extract_data():
    conn = connect("DataWarehouse")
    transform_data_into_tables(row,conn)
    count += 1
    if count == 2:
        break
