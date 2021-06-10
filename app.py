import traceback
import logging.config
from flask import Flask
from flask import render_template, request, redirect, url_for
import config.config as config

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

@app.route("/", methods=['GET', 'POST'])
def index():
    selectDate = ['Select Date', 'January', 'March']
    
    if selectDate == "January":
        return render_template('january.html')
    else:
        return render_template('index.html')
    
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
    
if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], host ='0.0.0.0', port=5000)

    
