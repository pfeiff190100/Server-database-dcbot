"""Module imports"""
import asyncio
import random
import time

import discord
from mcstatus import MinecraftServer
from threading import Thread

import editdatabase
import serverlookup
import embeds

class CMD():
    """functions to execute in the discord bot"""

    def __init__(self) -> None:
        """class variables"""

        self.data = []
        self.threadcounter = 0
        self.page = 0
        self.msg = ""

    async def getrandserver(self, ctx):
        """returns random servers out of the database"""

        player_online = 0
        tries = 0
        message = await ctx.channel.send("checking hostnames....")
        while player_online < 1:
            hostname = editdatabase.Databasemanager().get(random.randint(0, int(editdatabase
                                                                                .Databasemanager()
                                                                                .lengh())))
            try:
                server = MinecraftServer.lookup(hostname + ":25565")
                status = server.status()
                player_online = status.players.online
            except IOError:
                pass
            tries += 1
            await message.edit(content=f"looking for players ip:{hostname} " + \
                               f"| tries: {tries}")
        print(f"found server ip:{hostname} with {player_online}"+ \
              " player(s) online")

        await message.delete()
        
        await embeds.embedprint().ri_embed(ctx, status, hostname)

    async def get_info(self, ctx, message):
        """gets info about a specific server"""
        debugmsg = await ctx.channel.send("trying to get info about the server")
        try:
            server = MinecraftServer.lookup(message)
            status = server.status()
            await debugmsg.delete()
        except IOError:
            try:
                server = MinecraftServer.lookup(message + ":25565")
                status = server.status()
                await debugmsg.delete()
            except IOError:
                await debugmsg.edit(content="server was not reachable")

        await embeds.embedprint().ri_embed(ctx, status, message)


    async def searchservers(self, ctx):
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
                pt = Thread(target=lookup.main)
                ping_threads.append(pt)
                pt.start()
                self.threadcounter += 1
                outadresses.clear()

        for pt in ping_threads:
            pt.join()

        print(f"found {len(self.data)} servers with players online " +
                f"out of {editdatabase.Databasemanager().lengh()}")

        await infomsg.delete()

        await ctx.channel.send(f"found {len(self.data)} servers with players online " +
                f"out of {editdatabase.Databasemanager().lengh()} use -online to view")
        editdatabase.Databasemanager().onserverssave(self.data)

    async def showembed(self, ctx, message):
        """command to show embed"""
        counter = self.page * 10
        out = ""
        pagelengh = 0
        self.data = editdatabase.Databasemanager().onserversget()

        if message == "reverse":
            self.data.sort(key=lambda x: int(x[2]))
        elif message == None:
            self.data.sort(key=lambda x: int(x[2]), reverse=True)

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

    async def checkreaction(self, reaction, user):
        """functions to handle reactions"""
        if str(reaction.emoji) == "⬅️":
            if self.page != 0:
                self.page -= 1
                await self.updateembed()
                await reaction.message.remove_reaction(reaction.emoji, user)
        if str(reaction.emoji) == "➡️":
            if (self.page + 1) * 10 < len(self.data) - 1:
                self.page += 1
                await self.updateembed()
            await reaction.message.remove_reaction(reaction.emoji, user)

    async def updateembed(self):
        """class to update embed on reaction"""
        out = ""
        pagelengh = 0
        counter = self.page * 10
        embededit = discord.Embed(title="Servers", description=f"found {len(self.data)} servers with players online", color=0xFF7373)
        while(counter < len(self.data) and pagelengh < 10):
            out += f"{counter + 1}. IP: {self.data[counter][0]} | version: " +\
                   f"{self.data[counter][1][0:20]} | players: {self.data[counter][2]} \n"
            counter += 1
            pagelengh += 1
        embededit.add_field(name=f"Page: {self.page + 1}", value=out,
                            inline=False)
        await self.msg.edit(embed=embededit)
        out = None
