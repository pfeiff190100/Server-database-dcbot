import databasecmd ,editdatabase, discord
from discord.ext import commands
from mcstatus import MinecraftServer


class authenticate(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def rand (self, ctx):
        await databasecmd.CMD.getrandserver(ctx)        
  
    @commands.command()
    async def online (self, ctx):
        server_id = 1
        page = 0
        counter = 0
        lenghcount = 0
        out = ""
        data = []
        #int(editdatabase.Databasemanager().lengh()
        while (server_id < 50):
            hostname = editdatabase.Databasemanager().get(server_id)
            try:
                server = MinecraftServer.lookup(hostname + ":25565")
                status = server.status()
                player_online = status.players.online
            except:
                pass    
            if(player_online > 0):
                data.append((hostname, status.version.name, status.players.online))
            server_id += 1
            
        data.sort(key=lambda x:x[2], reverse=True)
        counter = page * 5
        """embed for displaying infos"""
        embedVar = discord.Embed(title="Servers", description="A list of servers with players online")
        while(counter < len(data) and lenghcount < 5):
            out += f"{counter + 1}. IP: {data[counter][0]} | version: {data[counter][1]} | players: {data[counter][2]} \n"
            counter += 1
            lenghcount += 1
        embedVar.add_field(name=f"Page: {page + 1}", value=out ,inline=False)
        msg = await ctx.channel.send(embed=embedVar)   
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

                    
    @commands.command()
    async def clear (self, ctx):
        def is_me(m):
            return m.author == self.client.user
        
        deleted = await ctx.channel.purge(limit=200, check=is_me)
        await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))

def setup(client):
    client.add_cog(authenticate(client))