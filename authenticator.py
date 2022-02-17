import databasecmd ,serverlookup, discord, time, editdatabase
from discord.ext import commands
from threading import Thread

class authenticate(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.data = []
        self.threadcounter = 0
        
    @commands.command()
    async def rand (self, ctx):
        await databasecmd.CMD.getrandserver(ctx)        
  
    @commands.command()
    async def online (self, ctx):
        page = 0
        counter = 0
        pagelengh = 0
        out = ""
        outadresses = []
        host_count = 1
        threadlengh = 10
        #int(editdatabase.Databasemanager().lengh())
        while host_count < 1000:
            while self.threadcounter > 100:
                time.sleep(0.1)
            outadresses.append(editdatabase.Databasemanager().get(host_count))
            if len(outadresses) >= threadlengh:
                lookup = serverlookup.Ping(threadlengh, outadresses.copy(), self)
                Thread(target=lookup.main).start()
                self.threadcounter += 1
                outadresses.clear()
            host_count += 1
        print(self.data)
            
        self.data.sort(key=lambda x:x[2], reverse=True)
        counter = page * 5
        """embed for displaying infos"""
        embedVar = discord.Embed(title="Servers", description="A list of servers with players online")
        while(counter < len(self.data) and pagelengh < 10):
            out += f"{counter + 1}. IP: {self.data[counter][0]} | version: {self.data[counter][1]} | players: {self.data[counter][2]} \n"
            counter += 1
            pagelengh += 1
        embedVar.add_field(name=f"Page: {page + 1}", value=out ,inline=False)
        msg = await ctx.channel.send(embed=embedVar)   
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

    async def on_reaction(self, reaction, user):
        print(reaction.message)
        msg = reaction.message
        print(msg.author)

def setup(client):
    client.add_cog(authenticate(client))