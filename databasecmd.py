"""Module imports"""
import time
from threading import Thread

import requests

import editdatabase
import serverlookup


class CMD():
    """functions to execute in the discord bot"""

    def __init__(self) -> None:
        """class variables"""

        self.data = []
        self.threadcounter = 0
        self.players = ""


    async def onlinecmd(self, ctx):
        """class to search through the hole database for servers with players online"""
        self.data.clear()
        threadlengh = 10
        adresses = editdatabase.Databasemanager().all()
        outadresses = []
        ping_threads = []

        infomsg = await ctx.channel.send("searching for servers with" +
                                         " players online")

        for adress in adresses:
            while self.threadcounter > 200:
                time.sleep(0.1)
            outadresses.append(adress)
            if len(outadresses) >= threadlengh:
                lookup = serverlookup.Ping(threadlengh, outadresses.copy(),
                                           self)
                pingthread = Thread(target=lookup.main)
                ping_threads.append(pingthread)
                pingthread.start()
                self.threadcounter += 1
                outadresses.clear()

        for pingthread in ping_threads:
            pingthread.join()

        print(f"found {len(self.data)} servers with players online " +
                f"out of {editdatabase.Databasemanager().lengh()}")

        await infomsg.delete()

        await ctx.channel.send(f"found {len(self.data)} servers with players online " +
                f"out of {editdatabase.Databasemanager().lengh()} use -online to view")
        editdatabase.Databasemanager().onserverssave(self.data)


    def getplayernames(self, server):
        """Looping through user query server (12 players) as long it doesnt have all playernames"""
        status = server.status()
        online = status.players.online

        if online == 0 and status.players.sample is None:
            return "no players online"
        elif online > 0 and status.players.sample is None:
            return "No responce"

        self.players = [item.name for item in status.players.sample]


        if len(self.players) == 0:
            return"responce list is empty"

        if online > 12:
            if len(self.players) == 1:
                return f"server modified responce: {self.players[0]}"
            while len(self.players) < online:
                status = server.status()
                for i in status.players.sample:
                    if i.name not in self.players:
                        self.players.append(i.name)
        return self.players


    def geolocation(self, ipaddress):
        """gets the geolocation of the server"""

        request_url = 'http://ip-api.com/json/' + ipaddress
        response = requests.get(request_url).json()

        if response['status'] == 'fail' and len(ipaddress.split(":")) > 1:
            request_url = 'http://ip-api.com/json/' + ipaddress.split(":")[0]
            response = requests.get(request_url).json()

        georesult = response

        if str(georesult['status']) == "success":
            flag = ":flag_" +  georesult["countryCode"].lower() + ":"
            return f"Country: {georesult['country']} {flag} | state: {georesult['regionName']}" + \
                f"| city: {georesult['city']} | IPv4: {georesult['query']} \n" + \
                f"ISP: {georesult['isp']} | timezone: {georesult['timezone']}"
        elif str(georesult['status']) == "fail":
            return f"failed to get geolocation of {self.georesult['query']}"
