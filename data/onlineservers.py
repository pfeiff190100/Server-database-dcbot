"""module imports"""
import datetime

import sqlalchemy
import datetime
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()

class Server(Base):
    """creating Server"""

    __tablename__ = "onlineservers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    hostname = sqlalchemy.Column(sqlalchemy.String)
    version = sqlalchemy.Column(sqlalchemy.String)
    onplayer = sqlalchemy.Column(sqlalchemy.Integer)
    timestamp = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)