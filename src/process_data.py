import string
from datetime import datetime, timedelta

import logging.config
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from gensim import corpora
from gensim.test.utils import common_corpus, common_dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel

import logging.config

# configure logger
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

# function to load data
def load_tweet_data(data_path = '../data/external/constructs.csv'):
    """Load data from S3 Bucket. 

    Args:
        s3path_str: str - name and path of the S3 bucket.

    Returns:
        tweet_data: dataframe - dataframe of all the tweets.
    """    
    
    logger.debug("Load data from path.")
    
    tweet_data = pd.read_csv(data_path)
    
    if len(tweet_data) > 0:
        logger.info("Dataset was loaded with %s rows", len(tweet_data))
    else: 
        logger.warning("Dataset is empty or did not load correctly!")
    
    return tweet_data

# function to remove duplicates
def remove_duplicates(df):
    """Remove any rows with duplicate text.
    
    Args: 
        df: dataframe of tweet data.
        
    Returns: 
        tweet_data: dataframe - dataframe without duplicate text entries.
    """
    
    logger.debug("Drop duplicate rows.")
    
    tweet_data = df.drop_duplicates(subset=['read_text_clean2'], keep='first')
    
    logger.info("%s rows were dropped", len(df) - len(tweet_data))
    
    return(tweet_data)

# function to format dates
def format_dates(df):
    """Format the 'create_at' data column to contain the month, day, and year only.
    
    Args: 
        df: dataframe - dataframe of the tweet_data.
        
    Returns: 
        df: dataframe - tweet data with a revised date column.
    """
    
    logger.debug("Format date column.")
    
    df['date'] = df['created_at'].str.split(' ').str[1:3]
    df['date'] = df['date'].str.join(' ')
    df['date'] = df['date'].astype(str)
    
    df['date'] = pd.to_datetime(df['date'] + ' 2020', format='%b %d %Y', errors='coerce')
    
    logger.info("New column created.")
    
    return df

# function to select timeframe of interest (+ 15 days)
def timeframe(df, input_date = '2020-01-01'):
    """Subset starting at the input_date + the next 30 days
    
    Args:
        df: dataframe - dataframe of the tweet_data.
        input_date: str - string of the date to subset in the format "2020-01-01".
    
    Returns: 
        df: dataframe - subset of the dataframe based on the input_date.
        input_date: str - date used to subset. This will be used as a file name for saved outputs.
    """
    
    usr_input = pd.to_datetime(input_date)
    
    logger.debug("Subset dataframe by the input_date + 15 days.")

    df = df[(df['date'] >= usr_input) & (df['date'] < (usr_input + timedelta(days=15)))]

    logger.info("Dataframe has been subset.")
    
    return df, input_date
    
# function to clean text 
def clean_text(tweets, stop_words_list, exclude, lemma):
    """Clean text data by removing punctuation and implementing lemmatization.
    
    Args:
        tweets: dataframe - dataframe subset by time.
        stop_words_list: list - list of words to remove from the analysis.
        exclude: set - set of non-alphanumeric characters to remove.
        lemma: nltk method to lemmatize text.
    
    Returns:
        doc_clean: dataframe - dataframe with processed text.
    """

    logger.debug("Begin text processing.")
    
    logger.info("Tokenize and Remove stop words")
    stop_free = " ".join([i for i in word_tokenize(tweets) if i not in stop_words_list])
    
    logger.info("Remove punctuation.")
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    
    logger.info("Lemmatize words.")
    doc_clean = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    
    return doc_clean

# function to create document term matrix and dictionary corpus 
def create_dictionary(df):
    """Create dictionary and a matrix of the terms per document.
    
    Args: 
        df: dataframe - processed dataframe.
    
    Returns:
        dictionary: corpora.dictionary - dictionary mapping each term to it's integer id.
        doc_term_matrix: list - bag of words matrix with frequency of each term mapped to dictionary id.
    
    """
    
    logger.debug("Create dictionary.")
    
    dictionary = corpora.Dictionary(df)
    
    logger.info("Dictionary created.")

    logger.debug("Create document term matrix.")
    
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in df]
    
    logger.info("Document term matrix created.")
    
    return dictionary, doc_term_matrix


