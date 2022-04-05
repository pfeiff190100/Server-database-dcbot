"""module imports"""
from discord.ext import commands

import databasecmd
import randcmd
import detailscmd
import listcmd


class DCcmd(commands.Cog):
    """discord commands"""

    def __init__(self, client):
        """init func"""
        self.client = client
        self.cmd = databasecmd.CMD()
        self.randcmd = randcmd.Rand()
        self.detailscmd = detailscmd.Details()
        self.listcmd = listcmd.Listserver()

    @commands.command()
    async def rand (self, ctx):
        """command to get random servers out of database"""
        await self.randcmd.main(ctx)

    @commands.command()
    async def onlinelookup (self, ctx):
        """command to get servers with players online"""
        await self.cmd.onlinecmd(ctx)

    @commands.command()
    async def online (self, ctx, message=None):
        """command to get servers with players online"""
        await self.cmd.showembed(ctx, message)

    @commands.command()
    async def details(self, ctx, message=None):
        """command to get details about a server"""
        await self.detailscmd.main(ctx, message)

    @commands.command()
    async def list(self, ctx, message=None, properties=None):
        """command to List specific servers"""
        await self.listcmd.main(ctx, message, properties)

    async def on_reaction(self, reaction, user):
        """on reaction"""
        await self.cmd.checkreaction(reaction, user)

def setup(client):
    """setup"""
    client.add_cog(DCcmd(client))
