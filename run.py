import os
import argparse
import re

import logging
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

import logging.config
import config.config as config

# configure logging
logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from src.add_topics_db import create_db, topics
from src.s3_upload import parse_s3, connect_s3

# define variables to connect to mysql
conn_type = "mysql+pymysql"
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
db_name = os.getenv("DATABASE_NAME")

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--s3', default=False,
                        help="If used, will download data from S3")
    parser.add_argument('--mysql', default=False,
                        help="If used, will download data from S3")
    parser.add_argument('--connect_type', default='download', 
                        help="If used, will download data from S3")
    parser.add_argument('--s3path', default='s3://2021-msia423-Hutch-Meghan/tweets.csv',
                        help="If used, upload data to the specified s3 path")
    parser.add_argument('--local_path', default='data/tweet.csv',
                        help="Where to load data to in S3")
    parser.add_argument('--train_model', default=False,
                        help="Where to load data to in S3")
    args = parser.parse_args()
    
    if args.s3:
        # connect to s3
        connect_s3(args.connect_type, args.s3path, args.local_path)
    
    if args.mysql:
        # connect to mysql database
        engine_string = f"{conn_type}://{user}:{password}@{host}:{port}/{db_name}"

        # create database for storing raw data
        engine = create_db(engine_string)

        Session = sessionmaker(bind=engine)  
        session = Session()