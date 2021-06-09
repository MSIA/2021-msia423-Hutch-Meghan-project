import traceback
import logging.config
from flask import Flask
from flask import render_template, request, redirect, url_for
import config.config as config

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database session
#from src.add_tweets import create_db, topics


#from src.add_tweets import create_db, topics#, AppManager
#tweet_app = AppManager(app)
#from src.add_songs import Tracks, TrackManager
#track_manager = TrackManager(app)

@app.route("/", methods=['GET', 'POST'])
def index():
    selectDate = ['Select Date', 'January', 'March']
    
    if selectDate == "January":
        return render_template('january.html')
    else:
        return render_template('index.html')
    
    #if request.method == 'POST':
    #    january = request.form['january']
    #    return redirect(url_for('january'))
    #else:
    #    return render_template('index.html')
    
    

@app.route("/january")
def january():
    return render_template("january.html")

@app.route("/march")
def march():
    return render_template("march.html")

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        select = request.form.get('selectDate')
        if select == "January":
            return redirect(url_for('january'))
        if select == "March":
            return redirect(url_for("march"))
        

#if __name__ == "__main__":
#    app.run()
    


#@app.route('/')
#def index():
#    """Main view that lists songs in the database.

#    Create view into index page that uses data queried from Track database and
#    inserts it into the msiapp/templates/index.html template.

#    Returns: rendered html template

#    """

    #try:
    #    tracks = track_manager.session.query(Tracks).limit(app.config["MAX_ROWS_SHOW"]).all()
    #    logger.debug("Index page accessed")
    #    return render_template('index.html', tracks=tracks)
    #except:
    #    traceback.print_exc()
    #    logger.warning("Not able to display tracks, error page returned")
    #    return render_template('error.html')


#@app.route('/add', methods=['POST'])
#def add_entry():
#    """View that process a POST with new song input

#    :return: redirect to index page
#    """

    #try:
    #    track_manager.add_track(artist=request.form['artist'], album=request.form['album'], title=request.form['title'])
    #    logger.info("New song added: %s by %s", request.form['title'], request.form['artist'])
    #    return redirect(url_for('index'))
    #except:
    #    logger.warning("Not able to display tracks, error page returned")
    #    return render_template('error.html')

    
if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], host ='0.0.0.0', port=5000)

    
