"""Module imports"""
import time
from threading import Thread

import discord

import editdatabase
import serverlookup


class CMD():
    """functions to execute in the discord bot"""

    def __init__(self) -> None:
        """class variables"""

        self.data = []
        self.threadcounter = 0
        self.players = ""
        self.page = 0
        self.msg = ""


    async def onlinecmd(self, ctx):
        """class to search through the hole database for servers with players online"""
        self.data.clear()
        self.page = 0
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

                 


    async def showembed(self, ctx, message):
        """shows a embed based on the database"""
        self.data = editdatabase.Databasemanager().onserversget()

        if message == "reverse":
            self.data.sort(key=lambda x: int(x[2]))
        elif message is None:
            self.data.sort(key=lambda x: int(x[2]), reverse=True)

        await self.onembed(ctx)

    async def checkreaction(self, reaction, user):
        """functions to handle reactions"""
        if str(reaction.emoji) == "⬅️":
            if self.page != 0:
                self.page -= 1
                await self.updatoneembed()
                await reaction.message.remove_reaction(reaction.emoji, user)
        if str(reaction.emoji) == "➡️":
            if (self.page + 1) * 10 < len(self.data) - 1:
                self.page += 1
                await self.updatoneembed()
            await reaction.message.remove_reaction(reaction.emoji, user)


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

    async def onembed(self, ctx):
        """command to show embed"""
        counter = self.page * 10
        out = ""
        pagelengh = 0

        # embed for displaying info
        embed = discord.Embed(title="Servers", description=f"found {len(self.data)} servers with" +
                                                           " players online", color=0xFF7373)
        while counter < len(self.data) and pagelengh < 10:
            out += f"{counter + 1}. IP: {self.data[counter][0]} | version: {self.data[counter][1][0:50]} | players: {self.data[counter][2]} \n"
            counter += 1
            pagelengh += 1
        embed.add_field(name=f"Page: {self.page + 1}", value=out,
                           inline=False)
        self.msg = await ctx.channel.send(embed=embed)
        await self.msg.add_reaction("⬅️")
        await self.msg.add_reaction("➡️")

    async def updatoneembed(self):
        """class to update embed on reaction"""
        out = ""
        pagelengh = 0
        counter = self.page * 10

        embededit = discord.Embed(title="Servers", description=f"found {len(self.data)} servers with players online", color=0xFF7373)
        while(counter < len(self.data) and pagelengh < 10):
            out += f"{counter + 1}. IP: {self.data[counter][0]} | version: " +\
                   f"{self.data[counter][1][0:50]} | players: {self.data[counter][2]} \n"
            counter += 1
            pagelengh += 1
        embededit.add_field(name=f"Page: {self.page + 1}", value=out,
                            inline=False)
        await self.msg.edit(embed=embededit)
        out = None
