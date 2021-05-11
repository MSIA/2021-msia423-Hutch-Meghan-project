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

class tweets(Base):
    """Create a data model for the database to store annotated tweets"""

    __tablename__ = 'tweets'

    read_tweet_id = Column(Integer, primary_key=True)
    created_at = Column(Integer, primary_key=False)
    user_location_id = Column(String(100), unique=False, nullable=False)
    coordinates = Column(String(100), unique=False, nullable=False)
    place = Column(String(100), unique=False, nullable=False)
    read_text_clean2 = Column(String(300), unique=False, nullable=False)
    Perceived_susceptibility = Column(Integer, primary_key=False)
    Perceived_severity = Column(Integer, primary_key=False)
    Perceived_benefits = Column(Integer, primary_key=False)
    Perceived_barriers = Column(Integer, primary_key=False)

    def __repr__(self):
        return '<tweet %r>' % self.read_text_clean2
    
    logger.debug("Create table and columns for raw data.")
    logger.info("Database table created.")

def create_db(engine_string: str) -> None:
    """Create database from provided engine string

    Args:
        engine_string: str - Engine string

    Returns: None

    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.debug("Attempting to create database from engine string.")
    logger.info("Database created.")
