"""Module import"""
from mcstatus import MinecraftServer

class Ping():
    """ping minecraft server"""

    def __init__(self, _threads, _hostname, cmd) -> None:
        self.threads = _threads
        self.hostname = _hostname
        self.tcount = cmd

    def main(self):
        """pings servers and checks if there are any players on the server"""
        counter = 0
        player_online = 0
        while counter < self.threads:
            try:
                server = MinecraftServer.lookup(self.hostname[counter] +
                                                ":25565")
                status = server.status()
                player_online = int(status.players.online)
            except IOError:
                pass
            if player_online > 0:
                self.tcount.data.append((self.hostname[counter], status.version.name,
                             player_online))
            counter += 1

        self.tcount.threadcounter -= 1
