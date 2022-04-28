"""module imports"""
import sqlalchemy
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()

class Server(Base):
    """creating Server"""

    __tablename__ = "server"

    server_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    server_hostname = sqlalchemy.Column(sqlalchemy.String)
