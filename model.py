import os
import argparse
import re

import logging
import string
import yaml
import random
import pandas as pd
import numpy as np
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from gensim import corpora
from gensim.test.utils import common_corpus, common_dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.colors as mcolors
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sklearn.model_selection import train_test_split


from src.process_data import load_tweet_data, remove_duplicates, format_dates, timeframe, clean_text, create_dictionary
from src.train_lda import topic_eval, get_max_k, get_doc_topic_matrix, create_topics_table, train_lda
from src.viz_topics import create_word_clouds
from src.add_topics_db import create_db, Topics
from src.s3_upload import parse_s3, connect_s3
import logging.config
import config.config as config

# configure logging
logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# load and parse yaml file.
a_yaml_file = open("config/model-meta.yaml")
config = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

if __name__ == '__main__':

# Prepare methods for text processin
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    # create list of stop words
    alphabet_remove = list(string.ascii_lowercase)
    number_remove = list(range(0, 9999))
    number_remove = map(str, number_remove) 
    number_remove = list(number_remove)

    stop_words_list = number_remove + alphabet_remove
    
    # Process data
    tweet_data = load_tweet_data(data_path = 'data/external/constructs.csv')
    logger.debug("Randomly sample rows to reduce dataframe and speed up modeling.")
    train, tweet_data = train_test_split(tweet_data, test_size=config['process_data']['sample_data']['test_size'],
                                         random_state=config['process_data']['sample_data']['random_state'])
        
    logger.info("Dataframe sampled with %s rows", len(tweet_data))
    tweet_data = remove_duplicates(tweet_data)
    tweet_data_formatted = format_dates(tweet_data)

    # Run First Analysis.
    logger.info("Running first analysis.")

    tweet_data_subset, input_date = timeframe(tweet_data_formatted, input_date = config['process_data']['time_frame']['time_frame1'])
    logging.info("Length of time sliced dataframe is %s rows", len(tweet_data_subset))

    doc_clean = [clean_text(tweets, stop_words_list, exclude, lemma).split() for tweets in tweet_data_subset['read_text_clean2']]

    dictionary, doc_term_matrix = create_dictionary(doc_clean)

    max_k, cov_model, coherence_score, doc_topic_df, top_tweets, input_date = train_lda(doc_clean, doc_term_matrix, dictionary, top_k = config['tune_model']['k_topics'], input_date = config['process_data']['time_frame']['time_frame1'], tweet_df = tweet_data_subset, coherence_score_method = config['tune_model']['coherence_score_method'], random_state = config['tune_model']['random_state'])

    ## visualize model 
    create_word_clouds(cov_model, input_date)

    logger.debug("Connect to mysql engine string.")
    engine_string = f"{conn_type}://{user}:{password}@{host}:{port}/{db_name}"

    engine = create_db(engine_string)

    logger.info("Save top_tweets table to MYSQL")
    top_tweets.to_sql(name='topics', con=engine, if_exists = 'append', index=False)

    # Run Second Analysis
    logger.info("Running second analysis.")
    tweet_data_subset, input_date = timeframe(tweet_data_formatted, input_date = config['process_data']['time_frame']['time_frame2'])
    logging.info("Length of time sliced dataframe is %s rows", len(tweet_data_subset))

    doc_clean = [clean_text(tweets, stop_words_list, exclude, lemma).split() for tweets in tweet_data_subset['read_text_clean2']]

    dictionary, doc_term_matrix = create_dictionary(doc_clean)

    max_k, cov_model, coherence_score, doc_topic_df, top_tweets, input_date = train_lda(doc_clean, doc_term_matrix, dictionary, top_k = config['tune_model']['k_topics'], input_date = config['process_data']['time_frame']['time_frame2'], tweet_df = tweet_data_subset, random_state = config['tune_model']['random_state'], coherence_score_method = config['tune_model']['coherence_score_method'])

    ## visualize model 
    create_word_clouds(cov_model, input_date)

    logger.debug("Connect to mysql engine string.")
    engine_string = f"{conn_type}://{user}:{password}@{host}:{port}/{db_name}"

    engine = create_db(engine_string)

    logger.info("Save top_tweets table to MYSQL")
    top_tweets.to_sql(name='topics', con=engine, if_exists = 'append', index=False)

    Session = sessionmaker(bind=engine)  
    session = Session()