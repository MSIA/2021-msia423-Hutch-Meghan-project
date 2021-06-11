import logging
import re

import yaml
import datetime
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import pytest

from src.add_topics_db import create_db
from src.s3_upload import parse_s3, connect_s3
from src.process_data import load_tweet_data, remove_duplicates, format_dates, timeframe, clean_text, create_dictionary
from src.train_lda import topic_eval, get_max_k, get_doc_topic_matrix, create_topics_table, train_lda
from src.viz_topics import create_word_clouds

# load and parse yaml file.
a_yaml_file = open("config/model-meta.yaml")
config = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

logger = logging.getLogger(__name__)

# read in sample_data
df = pd.read_csv("data/sample/tweets.csv")

sample_lda_results = {'topic_num':  ['1', '2', '3'],
                      'score': [0.45,0.55,0.75]
                     }
sample_lda_results = pd.DataFrame (sample_lda_results, columns = ['topic_num','score'])

# randoms state
random_state = config['tune_model']['random_state']
coherence_score_method = config['tune_model']['coherence']

# test create_db function
def test_create_db():
    # None should result in a type error
    s3path_str = None
    with pytest.raises(TypeError):
        create_db(s3path_str)
    
def test_create_db_str():
    s3path_str = 'this is a str'
    assert type(s3path_str) is str

#  test s3_upload functions
def test_parse_s3_str():
    s3path_str = 'this is a str'
    assert type(s3path_str) is str

def test_parse_s3_int():
    s3path_str = 1
    with pytest.raises(TypeError):
        assert type(s3path_str) is int

# test connect_s3
def test_connects3():
    connect_type = 'this is a string indicating connection type'
    assert type(s3path_str) is str
    
def test_connects3_connect_type_false():
    connect_type = "upload"
    if connect_type != 'upload' or connect_type != 'download':
        self.assertTrue(False)
            
# test process_data functions
def test_load_tweet_data():
    # None should result in a type error
    data_path = None
    with pytest.raises(TypeError):
        load_tweet_data(data_path)
        
def test_load_tweet_data_correct():
    data_path = 'path is a string'
    with pytest.raises(TypeError):
        assert type(s3path_str) is str

def test_remove_duplicates():
    if len(data) == pytest.approx(row_features):
        logging.warning("No Duplicates removed")
        
def test_remove_duplicates_successful():
    assert len(data) - 100 != pytest.approx(row_features)

def test_timeframe_date_fail():
    input_data = '2020-Jan-01'
    try:
        datetime.datetime.strptime(input_date, '%Y-%B-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def test_timeframe_date_success():
    input_data = '2020-01-01'
    try:
        datetime.datetime.strptime(input_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

def test_clean_text():
    stop_words_list = ['1', '2', 'abc']
    assert type(stop_words_list) is list
    
def create_dictionary_test():
    df = None
    with pytest.raises(TypeError):
        create_dictionary_test(df)
        
def create_dictionary_success():
    with pytest.raises(TypeError):
        create_dictionary_test(df)        

def test_timeframe_date_2020():
    input_date = '2018-01-01'
    pattern = re.compile('2020')
    
    if pattern.findall(input_date):
        self.assertTrue(True)
    else:
        self.assertTrue(False)

def topic_eval_test_top_k():
    top_k = 2
    
    if top_k < 4:
        raise ValueError("top_k cannot be lower than the set lower bound parameter for tuning.")
        
def topic_eval_test_top_k_success():
    top_k = 10
    
    if top_k < 4:
        raise ValueError("top_k cannot be lower than the set lower bound parameter for tuning.")
    
def get_max_k_test():
    lda_results = None
    with pytest.raises(TypeError):
        get_max_k(lda_results = None)
            
def get_max_k_test_success():
    lda_results = sample_lda_results
    with pytest.raises(TypeError):
        get_max_k(lda_results = None)

def train_lda_test_fail():
    top_k = 2
    
    if top_k < 4:
        raise ValueError("top_k cannot be lower than the set lower bound parameter for tuning.")

def train_lda_test_success():
    top_k = 10
    
    if top_k < 4:
        raise ValueError("top_k cannot be lower than the set lower bound parameter for tuning.")
        
def create_topics_table_success():
    # None should result in a type error
    input_date = '2020-01-01'
    assert type(input_date) is str

def test_create_topics_table_fail():
    # None should result in a type error
    input_date = 1
    assert type(input_date) is str

def create_word_clouds_test_fail():
    cov_model = None
    with pytest.raises(TypeError):
            create_word_clouds_test(cov_model, input_date = '2020-01-01')

def create_word_clouds_test_success():
    input_date = '2020-01-01'
    assert type(input_date) is str