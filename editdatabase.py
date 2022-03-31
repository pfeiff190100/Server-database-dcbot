"""module imports"""
import sqlalchemy
from servers import Base, Server
from onlineservers import Base as onBase, Server as onServer
from serverhistory import Base as Base_h, Server as server_h

class Databasemanager():
    """Databasemanage"""

    def __init__(self) -> None:
        """init func"""
        db_servers = sqlalchemy.create_engine("sqlite:///servers.db")
        Base.metadata.create_all(db_servers)
        self.session_servers = sqlalchemy.orm.sessionmaker()
        self.session_servers.configure(bind=db_servers)

        db_onlineservers = sqlalchemy.create_engine("sqlite:///onlineservers.db")
        onBase.metadata.create_all(db_onlineservers)
        self.session_onlineservers = sqlalchemy.orm.sessionmaker()
        self.session_onlineservers.configure(bind=db_onlineservers)

        db_serverhistory = sqlalchemy.create_engine("sqlite:///serverhistory.db")
        Base_h.metadata.create_all(db_serverhistory)
        self.session_serverhistory = sqlalchemy.orm.sessionmaker()
        self.session_serverhistory.configure(bind=db_serverhistory)

    def get(self, primary_key):
        """returns a specific id out of the database"""
        with self.session_servers() as session:
            return session.query(Server).get(primary_key).server_hostname

    def lengh(self):
        """returns the lengh of the database"""
        with self.session_servers() as session:
            return session.query(Server).count()

    def all(self):
        """returns all entries of the database"""
        hostnames = []
        with self.session_servers() as session:
            database = session.query(Server).all()
            for i in database:
                hostnames.append(i.server_hostname)
            return hostnames

    def onserverssave(self, data):
        """saves online servers to a database"""
        """with self.session_onlineservers() as session:
            database = session.query(onServer).all()
            with self.session_serverhistory() as hsession:
                if session.query(server_h).count() > 0:
                    for i in database:
                        hsession.add(server_h(hostname=i.hostname, modt=i.modt, onplayer=i.onplayer))
                    hsession.commit()"""

        with self.session_onlineservers() as session:
            for i in data:
                onserverdb = onServer(hostname=i[0], modt=i[1], onplayer=i[2])
                session.add(onserverdb)
            session.commit()

    def onserversget(self):
        """returns all entries of database"""
        serverinfo = []
        with self.session_onlineservers() as session:
            database = session.query(onServer).all()
            for i in database:
                serverinfo.append((i.hostname, i.modt, i.onplayer, i.timestamp))
            return serverinfo
