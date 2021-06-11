import logging.config
import numpy as np
import pandas as pd

from gensim import corpora
from gensim.test.utils import common_corpus, common_dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models.coherencemodel import CoherenceModel

# configure logger
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

# function to evaluate number of topics
def topic_eval(doc_clean, doc_term_matrix, dictionary, top_k, input_date):
    """Evaluate the number of topics (k) to choose via the highest coherence score.
    
    Args: 
        doc_clean: dataframe - dataframe with processed text.
        doc_term_matrix: list - bag of words matrix with frequency of each term mapped to dictionary id. 
        dictionary: corpora.dictionary - dictionary mapping each term to it's integer id.
        top_k: int - max number of topics to test.
        input_date: str - date that the user selected to subset the data.
    
    Return: 
        lda_results: dataframe - of scores from the k topic evaluation
    """

    logger.debug("Begin hyerparameter testing to determine number of k topics. to use in final model.")
    
    results = []
    
    for t in range(4, top_k):
        
        cov_model = LdaModel(corpus = doc_term_matrix, id2word = dictionary, num_topics = t, random_state=66826)

        cm = CoherenceModel(model=cov_model, dictionary=dictionary, texts=doc_clean, coherence='c_v')
        score = cm.get_coherence()
        tup = t, score
        results.append(tup)
    logger.info("Hyperparameter testing complete.")

    logger.debug("Save topic number and coherence score as a dataframe.")
    
    lda_results = pd.DataFrame(results, columns=['topic', 'score'])
    
    logger.debug("Evaluate whether the last tested k had the highest coherence score. If so, next iteration may want to increase k.")
    
    logger.debug("Generate a plot of coherence score by k topics.")
    
    return lda_results

def get_max_k(lda_results):
    
    logger.debug("Abstract topic_num with the max coherence score.")
    
    max_k = lda_results.iloc[lda_results['score'].argmax()][['topic']].astype(int)
    
    logger.info("Optimal number of k topics is: %s", max_k)
    
    return max_k
     
def get_doc_topic_matrix(lda_model, doc_term_matrix, tweet_df, input_date):
    """Caculates the topic probability of each tweet and then assigns the topic with the highest probability.
    
    Args: 
        lda_model: lda object - trained lda model object.
        doc_term_matrix: list - bag of words matrix with frequency of each term mapped to dictionary id. 
        tweet_df: dataframe - orgiinal dataframe of covid-19 tweets.
        input_date: str - date used to subset dataframe.
    
    Return: 
        doc_topic_max_df: dataframe - dataframe containing a row for each tweet with a column 'topic_num' indicating the topic with the highest probability for that tweet.
        doc_topic_df: dataframe - dataframe of tweets and their probabilities per topic.
        
    """
    
    logger.debug("Calculate topic probability of each tweet.")
    
    doc_topics = lda_model.get_document_topics(doc_term_matrix, minimum_probability=None, minimum_phi_value=None, per_word_topics=False)
    
    logger.info("Topic probability calculated.")

    doc_topic_max = []

    logger.debug("For each original tweet, assign a column with the topic_num containing the max probability of being associated with that tweet.")
    
    for d in range(len(doc_topics)):
        topic_df = pd.DataFrame(doc_topics[d])
        topic_df.columns = ['topic_num', 'prob']
        topic_df = topic_df.iloc[topic_df['prob'].argmax()]
        topic_df = pd.DataFrame(topic_df).transpose()
        tweet_data_subset_df = tweet_df.reset_index()
        timeframe_slice = tweet_data_subset_df[['read_text_clean2','Perceived_susceptibility', 'Perceived_severity', 'Perceived_benefits', 'Perceived_barriers']]
        topic_df = pd.concat([topic_df, timeframe_slice.reindex(topic_df.index)], axis=1, join="inner")
        doc_topic_max.append(topic_df)
        
    logger.info("New topic probability dataframe created.")
    
    doc_topic_max_df = pd.concat(doc_topic_max)
    
    logger.debug("Count the number of original health-belief annotations by topic_num.")
    
    doc_topic_df = doc_topic_max_df.copy()
    
    doc_topic_matrix = doc_topic_df.groupby(['topic_num'])['Perceived_susceptibility', 'Perceived_severity', 'Perceived_benefits','Perceived_barriers'].sum().reset_index()
    
    doc_topic_matrix['count'] = doc_topic_matrix['topic_num'].map(doc_topic_df['topic_num'].value_counts())
    
    logger.info("Matrix of topic_num and annotation counts generated.")
    
    logger.debug("Save Matrix to 'data/results' folder.")
    
    doc_topic_matrix.to_csv('data/results/' + input_date + '_topic_matrix.csv', index = False)
    
    logger.info("Matrix saved.")
    
    return doc_topic_matrix, doc_topic_df

def create_topics_table(doc_topic_df, input_date):
    """Creates a confusion-like-matrix to count annotations of the orginal tweets per highest probable topic.
    
        Args: 
            doc_topic_df: dataframe - dataframe of the tweets mapped to their highest probable topic.
            input_date: str - input_date will be added to a new column to indicate the time period that generated the topic.
        
        Returns:
            top_tweets: dataframe - dataframe containing counts of original annotations by topic_num.
    """
    
    logger.debug("Sort doc_topic_max_df in order of probability.")
    
    doc_topic_max_df_ordered = doc_topic_df.sort_values('prob', ascending=False)
    top_tweets = doc_topic_max_df_ordered.groupby('topic_num').head(3)
    top_tweets.sort_values('topic_num')

    logger.info("doc_topic_max_df sorted and renamed as top_tweets.")
    
    logger.debug("Add the input_date to the top_tweets dataframe.")
    
    top_tweets['date'] = input_date
    
    logger.info('Date is set to %s', input_date)
    
    logger.debug("Subset dataframe to keep only relevant columns.")
    
    top_tweets = top_tweets[['date', 'topic_num', 'prob', 'read_text_clean2', 'Perceived_susceptibility', 'Perceived_severity', 'Perceived_benefits', 'Perceived_barriers']]
    top_tweets.columns = ['date', 'topic_num', 'prob', 'tweet', 'Perceived_susceptibility', 'Perceived_severity', 'Perceived_benefits', 'Perceived_barriers']
    
    logger.info("Dataframe is subset and organized.")
    
    logger.debug("Save top_tweets dataframe to 'data/results' folder")
    
    top_tweets.to_csv('data/results/top_tweets_' +  input_date, index = False)
    
    logger.info("top_tweets saved.")
    
    return(top_tweets)

def train_lda(doc_clean, doc_term_matrix, dictionary, top_k, input_date, tweet_df):
    """Train the lda model on the max K found during topic evaluation.
    
    Args: 
        doc_clean: dataframe - dataframe with processed text.
        doc_term_matrix: list - bag of words matrix with frequency of each term mapped to dictionary id. 
        dictionary: corpora.dictionary - dictionary mapping each term to it's integer id.
        top_k: int - max number of topics to test.
        input_date: str - date that the user selected to subset the data.
        tweet_df: dataframe - original dataframe of tweets.
    
    Return: 
        max_k: int - integer indicating optimal number of k topics.
        cov_model: trained lda model object.
        coherence_score: int - return coherence score.
        doc_topic_max_df: dataframe - dataframe of each orignal tweet/annotation with the topic most associated with it.
    """
    
    # evaluate best k topics
    lda_results = topic_eval(doc_clean, doc_term_matrix, dictionary, top_k, input_date)
    
    # save plots
    s = pd.Series(lda_results.score.values, index=lda_results.topic.values)
    
    plt = s.plot()
    plt = plt.get_figure()
    plt.savefig("app/static/" + input_date + "_k_topics" + ".png")
    plt.clf()
    
    logger.debug("Determine optimal number of k topics.")
    # get k with highest coherence score
    max_k = get_max_k(lda_results)
    
    logger.info("%s is the optimal k", max_k)
    
    # train model with optimal k
    cov_model = LdaModel(corpus = doc_term_matrix, id2word = dictionary, num_topics = max_k, random_state=66826)
    
    # save trained model object
    logger.debug("Save trained LDA object.")
    
    cov_model.save('models/' + 'lda_cov_model' + '_' + input_date)
    
    logger.info("LDA object saved to 'model/' folder.")
    
    # get final coherence score
    cm = CoherenceModel(model=cov_model, dictionary=dictionary, texts=doc_clean, coherence='c_v')
    coherence_score = cm.get_coherence()
    
    logging.info("Coherence score: %s", coherence_score)
    
    if coherence_score < 0.50:
        logging.warning("Coherence Score is low. Test new k.")
          
    # determine topic with the highest probability for each tweet
    doc_topic_matrix, doc_topic_df = get_doc_topic_matrix(cov_model, doc_term_matrix, tweet_df, input_date)
    
    # create topics table
    top_tweets = create_topics_table(doc_topic_df, input_date)

    return max_k, cov_model, coherence_score, doc_topic_df, top_tweets, input_date