from threading import Thread
import discord, random
import editdatabase
from mcstatus import MinecraftServer
from discord.ext import commands

class authenticate(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def list (self, ctx, message=""):
        if (message == ""):
            await ctx.channel.send('an argument is required (get)')
        elif (message == "get"):
            player_online = 0
            tries = 0
            while(player_online < 1):
                hostname = editdatabase.Databasemanager(random.randint(0, int(editdatabase.Databasemanager(2).lengh()))).get()
                try:
                    server = MinecraftServer.lookup(hostname + ":25565")
                    status = server.status()
                    player_online = status.players.online
                except:
                    pass         
                tries +=1  
                print(tries, end="\r")     
            embedVar = discord.Embed(title="Server", description="with players online", color=0xff6ec7)
            embedVar.add_field(name="ip", value=hostname, inline=False)
            embedVar.add_field(name="Players online", value=status.players.online, inline=False)
            embedVar.add_field(name="Latency", value=status.latency, inline=False)
            await ctx.channel.send(embed=embedVar)
            
       
    
    @commands.command()
    async def clear (self, ctx):
        def is_me(m):
            return m.author == self.client.user
        
        deleted = await ctx.channel.purge(limit=200, check=is_me)
        await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))

def setup(client):
    client.add_cog(authenticate(client))