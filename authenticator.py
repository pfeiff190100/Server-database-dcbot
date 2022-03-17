"""module imports"""
from discord.ext import commands

import databasecmd


class DCcmd(commands.Cog):
    """discord commands"""

    def __init__(self, client):
        """init func"""
        self.client = client
        self.cmd = databasecmd.CMD()

    @commands.command()
    async def rand (self, ctx):
        """command to get random servers out of database"""
        await self.cmd.getrandserver(ctx)

    @commands.command()
    async def onlinelookup (self, ctx):
        """command to get servers with players online"""
        await self.cmd.searchservers(ctx)

    @commands.command()
    async def online (self, ctx, message=None):
        """command to get servers with players online"""
        await self.cmd.showembed(ctx, message)

    @commands.command()
    async def details(self, ctx, message=None):
        """command to get details about a server"""
        await self.cmd.getdetails(ctx, message)

    async def on_reaction(self, reaction, user):
        """on reaction"""
        msg = reaction.message
        await self.cmd.checkreaction(reaction, user)

def setup(client):
    """setup"""
    client.add_cog(DCcmd(client))
