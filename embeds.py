"""module imports"""
import urllib
import os
import discord

import databasecmd
import geolocation


class Embedmanager():
    """all embeds of the programm"""
    def __init__(self) -> None:
        pass

    async def randembed(self, ctx, status, hostname):
        """embed for rand and info command command"""

        path = "pics/rand.jpg"
        # gets the favicon of the minecraft server
        img_data = status.favicon
        if img_data is not None:
            response = urllib.request.urlopen(img_data)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open('pics/rand.jpg', 'wb') as file:
                file.write(response.file.read())
                file = discord.File('pics/rand.jpg', filename="rand.jpg")

        # embed for displaying infos

        embed = discord.Embed(title="Random server", description="motd: " +
                                 status.description, color=0x00008B)
        embed.add_field(name="ip", value=hostname, inline=True)
        embed.add_field(name="version", value=status.version.name,
                           inline=True)
        embed.add_field(name="Players online", value=status.players.online,
                           inline=False)
        embed.add_field(name="Latency in ms", value=status.latency,
                           inline=True)
        embed.set_image(url='attachment://rand.jpg')
        if img_data is not None:
            await ctx.channel.send(embed=embed, file=file)
        else:
            await ctx.channel.send(embed=embed)

    async def detailsembed(self, ctx, server, hostname):
        """embed for details command"""
        status = server.status()
        path = "pics/details.jpg"
        # gets the favicon of the minecraft server
        img_data = status.favicon
        if img_data is not None:
            response = urllib.request.urlopen(img_data)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open('pics/details.jpg', 'wb') as file:
                file.write(response.file.read())
                file = discord.File('pics/details.jpg', filename="details.jpg")

        # embed for displaying infos
        embed = discord.Embed(title="Details about a Server", description="motd: " +
                                 status.description, color=0xFFA500)
        embed.add_field(name="ip", value=hostname, inline=False)
        embed.add_field(name="version", value=status.version.name,
                           inline=True)
        embed.add_field(name="Latency in ms", value=status.latency,
                    inline=True)
        embed.add_field(name="Players online", value=status.players.online,
                           inline=False)
        embed.add_field(name="Player names", value=databasecmd.CMD().getplayernames(server),
                           inline=False)
        embed.add_field(name="Geolocation", value=geolocation.Serverlocation(hostname).main(),
                           inline=False)
        embed.set_image(url='attachment://details.jpg')
        if img_data is not None:
            await ctx.channel.send(embed=embed, file=file)
        else:
            await ctx.channel.send(embed=embed)
