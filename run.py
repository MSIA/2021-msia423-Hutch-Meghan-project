import os
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
import logging.config

# configure logging
logging.config.fileConfig('config/logging/local.conf')

from src.add_tweets import create_db, tweets

# define variables to connect to mysql
conn_type = "mysql+pymysql"
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
db_name = os.getenv("DATABASE_NAME")

# connect to mysql database
engine_string = f"{conn_type}://{user}:{password}@{host}:{port}/{db_name}"
engine = sqlalchemy.create_engine(engine_string)

# create database for storing raw data
create_db(engine_string)

Session = sessionmaker(bind=engine)  
session = Session()

# add a fake tweet to our database as an example
tweet = tweets(read_tweet_id=0,
                created_at="1900-01-01",
                user_location_id=999, 
                coordinates="long:123",
                place="Boston,MA",
                read_text_clean2="fake tweet",
                Perceived_susceptibility=999,
                Perceived_severity=999,
                Perceived_benefits=999,
                Perceived_barriers=999)  
session.add(tweet)
print(session.commit())
