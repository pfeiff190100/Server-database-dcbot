import databasecmd
from discord.ext import commands


class authenticate(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def list (self, ctx, message=""):
        if (message == "rand"):
            await databasecmd.CMD.getrandserver(ctx)            
        elif message == "active":
            await databasecmd.CMD.getserverplayer(ctx)
        else:
            await ctx.channel.send("missing arguments (rand)")
            
                
    @commands.command()
    async def clear (self, ctx):
        def is_me(m):
            return m.author == self.client.user
        
        deleted = await ctx.channel.purge(limit=200, check=is_me)
        await ctx.channel.send('Deleted {} message(s)'.format(len(deleted)))

def setup(client):
    client.add_cog(authenticate(client))