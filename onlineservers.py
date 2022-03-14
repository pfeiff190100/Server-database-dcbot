"""module imports"""
import sqlalchemy
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()

class Server(Base):
    """creating Server"""

    __tablename__ = "onlineservers"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    hostname = sqlalchemy.Column(sqlalchemy.String)
    modt = sqlalchemy.Column(sqlalchemy.String)
    onplayer = sqlalchemy.Column(sqlalchemy.Integer)
