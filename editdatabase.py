from http import server
import sqlalchemy
from servers import Base, Server
class Databasemanager():
    def __init__(self) -> None:
        #self.id = server_id
        db_connection = sqlalchemy.create_engine("sqlite:///servers.db")
        Base.metadata.create_all(db_connection)
        self.session_factory = sqlalchemy.orm.sessionmaker()
        self.session_factory.configure(bind=db_connection)

    def get(self, id):
        with self.session_factory() as session:
            return(session.query(Server).get(id).server_hostname)
    
    def lengh(self):
        with self.session_factory() as session:
            return(session.query(Server).count())