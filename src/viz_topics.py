import logging.config
import gensim 
import matplotlib.colors as mcolors
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt

# configure logger
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

def create_word_clouds(cov_model, input_date):
    """Create word clouds for each topic and save to app folder.
    
    Args: 
        cov_model: trained lda_model
        input_date: str - input date used to subset tweets, this will be used to name file.
    
    Returns: None
    """
    
    cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  

    cloud = WordCloud(background_color='white',
                      width=2500,
                      height=1800,
                      max_words=20,
                      colormap='tab10',
                      color_func=lambda *args, **kwargs: cols[i],
                      prefer_horizontal=1.0)

    logger.debug("Return topics for the lda model.")
    
    topics = cov_model.show_topics(formatted=False)
    
    n_topics = len(topics)
    
    sub_plot_row = n_topics/2
    
    logger.info("Topics object will contain the top significant terms associated with each topic.")

    fig, axes = plt.subplots(sub_plot_row,2, figsize=(10,10), sharex=True, sharey=True)

    logger.info("Return topics for the lda model in a word cloud.")
    
    for i, ax in enumerate(axes.flatten()):
        fig.add_subplot(ax)
        topic_words = dict(topics[i][1])
        cloud.generate_from_frequencies(topic_words, max_font_size=300)
        # If number of topics is not an even number, we delete the last subplot.
        if (sub_plot_row % 2) != 0:
            axes[(sub_plot_row-1),1].set_axis_off()
        plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=20))
        plt.gca().axis('off')
        plt.savefig('app/static/word_cloud_' + input_date + ".png", facecolor='w')
        plt.gca().imshow(cloud)
    
    logger.debug("Save word cloud images.")