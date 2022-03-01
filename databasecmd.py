"""Module imports"""
import random
import time
import urllib
from threading import Thread

import discord
from mcstatus import MinecraftServer

import editdatabase
import serverlookup


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
            except:
                pass
            tries += 1
            await message.edit(content=f"looking for players ip:{hostname}" + \
                               f"| tries: {tries}")
        print(f"found server ip:{hostname} with {player_online}"+ \
              " player(s) online")

        await message.delete()
        # gets the favicon of the minecraft server
        img_data = status.favicon
        if img_data is not None:
            response = urllib.request.urlopen(img_data)
            with open('image.jpg', 'wb') as file:
                file.write(response.file.read())
                file = discord.File("image.jpg")

        # embed for displaying infos

        embed = discord.Embed(title="Server", description="motd: " +
                                 status.description, color=0xff6ec7)
        embed.add_field(name="ip", value=hostname, inline=False)
        embed.add_field(name="version", value=status.version.name,
                           inline=False)
        embed.add_field(name="Players online", value=status.players.online,
                           inline=False)
        embed.add_field(name="Latency in ms", value=status.latency,
                           inline=False)
        embed.set_image(url='attachment://image.jpg')
        if img_data is not None:
            await ctx.channel.send(embed=embed, file=file)
        else:
            await ctx.channel.send(embed=embed)

    async def searchservers(self, ctx, message):
        """class to search through the hole database for servers with players online"""

        self.page = 0
        self.data.clear()

        out = ""
        outadresses = []

        counter = 0
        pagelengh = 0
        host_count = 1
        threadlengh = 10
        databaselengh = 5000

        infomsg = await ctx.channel.send("searching for servers with" +
                                         " players online")
        # int(editdatabase.Databasemanager().lengh())
        while host_count < databaselengh:
            while self.threadcounter > 200:
                time.sleep(0.1)
            outadresses.append(editdatabase.Databasemanager().get(host_count))
            if len(outadresses) >= threadlengh:
                lookup = serverlookup.Ping(threadlengh, outadresses.copy(),
                                           self)
                Thread(target=lookup.main).start()
                self.threadcounter += 1
                outadresses.clear()
            host_count += 1
        await infomsg.edit(content="waiting for all threads to finisch")

        while True:
            if self.threadcounter == 0:
                print(f"found {len(self.data)} servers with players online " +
                      f"out of {databaselengh}")
                break

        await infomsg.delete()

        if message == "reverse":
            self.data.sort(key=lambda x: int(x[2]))
        elif message == "top":
            self.data.sort(key=lambda x: int(x[2]), reverse=True)

        counter = self.page * 10

        # embed for displaying info
        embed = discord.Embed(title="Servers", description=f"found {len(self.data)} servers with" +
                                                           " players online", color=0xFF7373)
        while counter < len(self.data) and pagelengh < 10:
            out += f"{counter + 1}. IP: {self.data[counter][0]} | version: {self.data[counter][1]} | players: {self.data[counter][2]} \n"
            counter += 1
            pagelengh += 1
        embed.add_field(name=f"Page: {self.page + 1}", value=out,
                           inline=False)
        self.msg = await ctx.channel.send(embed=embed)
        await self.msg.add_reaction("⬅️")
        await self.msg.add_reaction("➡️")

    async def info(self, ctx, message):
        """class to get detailed infos about a specific ip which the user can enter"""
        await ctx.channel.send("info")
        print(message)
        time.sleep(300)
        await self.msg.delete()

    async def details(self, ctx, message):
        if message == None:
            await ctx.channel.send("Missing ip to perform this command")
            return

        msg = await ctx.channel.send("collecting information ....")
        hostname = message
        try:
            server = MinecraftServer.lookup(hostname + ":25565")
            status = server.status()
        except:
            await msg.edit(content=f"invalid ip {message}")     
        print(f"collecting information of {message}")
        
        await msg.delete()
        """gets the favicon of the minecraft server"""
        img_data = status.favicon
        if(img_data != None):
            response = urllib.request.urlopen(img_data)
            with open('img/details.jpg', 'wb') as f:
                f.write(response.file.read())   
                file = discord.File("img/details.jpg")        
        
        """embed for displaying infos"""
        embedVar = discord.Embed(title="Server", description="motd: " + status.description, color=0xff6ec7)
        embedVar.add_field(name="ip", value=hostname, inline=False)
        embedVar.add_field(name="version", value=status.version.name, inline=False)
        embedVar.add_field(name="Players online", value=status.players.online, inline=False)
        embedVar.add_field(name="Latency in ms", value=status.latency, inline=False)
        embedVar.set_image(url='attachment://details.jpg')
        if img_data != None:
            await ctx.channel.send(embed=embedVar, file= file)
        else:
            await ctx.channel.send(embed=embedVar)
        
        

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
                   f"{self.data[counter][1]} | players: {self.data[counter][2]} \n"
            counter += 1
            pagelengh += 1
        embededit.add_field(name=f"Page: {self.page + 1}", value=out,
                            inline=False)
        await self.msg.edit(embed=embededit)
