import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy
import logging
import pandas as pd


# code borrowed from Michael Fedell's SQLAchemy tutorial: https://github.com/MSIA/423-sqlalchemy-lab-activity

# the engine_string format
conn_type = "mysql+pymysql"
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
db_name = os.getenv("DATABASE_NAME")
engine_string = f"{conn_type}://{user}:{password}@{host}:{port}/{db_name}"
engine = sqlalchemy.create_engine(engine_string)
