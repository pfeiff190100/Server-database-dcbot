"""module imports"""
import sqlalchemy
from servers import Base, Server

class Databasemanager():
    """Databasemanage"""

    def __init__(self) -> None:
        """init func"""
        #self.id = server_id
        db_connection = sqlalchemy.create_engine("sqlite:///servers.db")
        Base.metadata.create_all(db_connection)
        self.session_factory = sqlalchemy.orm.sessionmaker()
        self.session_factory.configure(bind=db_connection)

    def get(self, primary_key):
        """returns a specific id out of the database"""
        with self.session_factory() as session:
            return session.query(Server).get(primary_key).server_hostname

    def lengh(self):
        """returns the lengh of the database"""
        with self.session_factory() as session:
            return session.query(Server).count()
