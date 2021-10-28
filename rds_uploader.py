from sqlalchemy import create_engine

DATABASE_TYPE = "postgresql"
DBAPI = "psycopg2"
ENDPOINT = "aicore-booking-project.c5oixetjusab.us-east-2.rds.amazonaws.com"
USER = "postgres"
PASSWORD = "Bookingproject2021"
PORT = 5432
DATABASE = "postgres"
engine = create_engine(
    f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"
)

engine.connect()

import pandas as pd

# from booking import BeginningStage()

df = pd.read_csv("hotels.csv")
df.to_sql("hotels.csv", engine, if_exists="replace")
