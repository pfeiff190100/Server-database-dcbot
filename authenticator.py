"""module imports"""
from discord.ext import commands

import databasecmd


class DCcmd(commands.Cog):
    """class to define commands"""

    def __init__(self, client):
        """init variables"""

        self.client = client
        self.cmd = databasecmd.CMD()

    @commands.command()
    async def rand(self, ctx):
        """command to get random server with players online"""

        await self.cmd.getrandserver(ctx)

    @commands.command()
    async def online(self, ctx, message="top"):
        """command to get all servers with players online"""
        await self.cmd.searchservers(ctx, message)

    @commands.command()
    async def info(self, ctx, message = ""):
        """command to get detailed info about a specific server"""
        await self.cmd.info(ctx, message)

    async def on_reaction(self, reaction, user):
        """func to execute code on reaction"""
        msg = reaction.message
        if str(msg.author) == "MC-servers#6007":
            await self.cmd.checkreaction(reaction, user)

def setup(client):
    """setup"""
    client.add_cog(DCcmd(client))
