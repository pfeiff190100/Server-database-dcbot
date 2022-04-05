"""Module imports"""

import discord

import editdatabase


class Listserver():
    """Listserver Class"""
    def __init__(self) -> None:
        self.data = []
        self.page = 0
        self.msg = ""

    async def main(self, ctx, message, properties):
        """search for server with specific properties"""
        if message == "version":
            database = editdatabase.Databasemanager().onserversget()
            for server in database:
                if server[1].find(properties) != -1:
                    self.data.append(server)
        await self.listembed(ctx)


    async def listembed(self, ctx):
        """embed for list func"""

        counter = self.page * 10
        out = ""
        pagelengh = 0

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
        await self.msg.add_reaction("⏮️")
        await self.msg.add_reaction("⏭️")
