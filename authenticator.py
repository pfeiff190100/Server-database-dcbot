import databasecmd
from discord.ext import commands

class authenticate(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cmd = databasecmd.CMD()
        
    @commands.command()
    async def rand (self, ctx):
        await self.cmd.getrandserver(ctx)        
  
    @commands.command()
    async def online (self, ctx, message="top"):
        await self.cmd.searchservers(ctx, message)

    async def on_reaction(self, reaction, user):
        msg = reaction.message
        if(str(msg.author) == "MC-servers#6007"):
            await self.cmd.checkreaction(reaction, user)

def setup(client):
    client.add_cog(authenticate(client))