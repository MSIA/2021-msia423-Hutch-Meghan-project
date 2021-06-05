import os
import argparse
import re

#import logging
#import sqlalchemy
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import Column, Integer, String, MetaData
#from sqlalchemy.orm import sessionmaker
#from flask_sqlalchemy import SQLAlchemy
import logging.config
import config.config as config

# configure logging
logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger('run')


#from src.add_tweets import create_db, tweets
from src.s3_upload import parse_s3, connect_s3

#connect_type = os.getenv("connect_type")
#s3path = os.getenv("s3path")
#local_path = os.getenv("local_path")

#connect_s3(connect_type="download", s3path="s3://2021-msia423-hutch-meghan/data/sample_tweets.csv", local_path="data/tweet.csv")

# define variables to connect to mysql
#conn_type = "mysql+pymysql"
#user = os.getenv("MYSQL_USER")
#password = os.getenv("MYSQL_PASSWORD")
#host = os.getenv("MYSQL_HOST")
#port = os.getenv("MYSQL_PORT")
#db_name = os.getenv("DATABASE_NAME")

# connect to mysql database
#engine_string = f"{conn_type}://{user}:{password}@{host}:{port}/{db_name}"
#engine = sqlalchemy.create_engine(engine_string)

# create database for storing raw data
#create_db(engine_string)

#Session = sessionmaker(bind=engine)  
#session = Session()

# add a fake tweet to our database as an example
#tweet = tweets(read_tweet_id=2,
#                created_at="1900-01-01",
#                user_location_id=999, 
#                coordinates="long:123",
#                place="Boston,MA",
#                read_text_clean2="fake tweet",
#                Perceived_susceptibility=999,
#                Perceived_severity=999,
#                Perceived_benefits=999,
#                Perceived_barriers=999)  
#session.add(tweet)
#print(session.commit())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sep', default=';',
                        help="CSV separator if using pandas")
    parser.add_argument('--pandas', default=False, action='store_true',
                        help="If used, will load data via pandas")
    parser.add_argument('--connect_type', default='download', 
                        help="If used, will download data from S3")
    parser.add_argument('--s3path', default='s3://2021-msia423-Hutch-Meghan/tweets.csv',
                        help="If used, upload data to the specified s3 path")
    parser.add_argument('--local_path', default='data/tweet.csv',
                        help="Where to load data to in S3")
    args = parser.parse_args()
    
    if args.pandas:
        download_from_s3_pandas(args.local_path, args.s3path, args.sep)
    else:
        connect_s3(args.connect_type, args.s3path, args.local_path)