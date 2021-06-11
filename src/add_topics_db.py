import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
import logging.config

# configure logger
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

Base = declarative_base()

# code adapted from Michael Fedell's SQLAchemy tutorial: https://github.com/MSIA/423-sqlalchemy-lab-activity

class Topics(Base):
    """Create a data model for the database to store topics for time periods."""

    __tablename__ = 'topics'

    read_tweet_id = Column(Integer, primary_key=True)
    date = Column(String(10), primary_key=False)
    topic_num = Column(Integer, primary_key=False)
    prob = Column(Integer, primary_key=False)
    tweet = Column(String(300), primary_key=False)
    Perceived_susceptibility = Column(Integer, primary_key=False)
    Perceived_severity = Column(Integer, primary_key=False)
    Perceived_benefits = Column(Integer, primary_key=False)
    Perceived_barriers = Column(Integer, primary_key=False)

    def __repr__(self):
        return '<topics %r>' % self.topic

def create_db(engine_string: str):
    """Create database from provided engine string.

    Args:
        engine_string: str - Engine string.

    Returns: 
        engine: sqlalchemy.engine.base.Engine - sqlalchemy connection from amazon rds  

    """
    logger.debug("Create table and columns for raw data.")
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.debug("Attempting to create database from engine string.")
    logger.info("Database created.")
    
    return engine

class TopicManager:

    def __init__(self, app=None, engine_string=None):
        """
        Args:
            app: Flask - Flask app
            engine_string: str - Engine string
        """
        if app:
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")

    def close(self) -> None:
        """Closes session
        Returns: None
        """
        self.session.close()
