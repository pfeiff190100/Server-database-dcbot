from mcstatus import MinecraftServer

class Ping():
    def __init__(self, _threads, _hostname, cmd) -> None:
        self.threads = _threads
        self.hostname = _hostname
        self.tcount = cmd

    def main(self):
        self.ping()
        self.tcount.threadcounter -= 1

    def ping(self):
        data = []
        counter = 0
        player_online = 0
        while (counter < self.threads):
            try:
                server = MinecraftServer.lookup(self.hostname[counter] + ":25565")
                status = server.status()
                player_online = status.players.online
            except:
                pass    
            if(player_online > 0):
                data.append((self.hostname[counter], status.version.name, status.players.online))
            counter += 1
        if data:  
            for i in data:
                self.tcount.data.append(i)