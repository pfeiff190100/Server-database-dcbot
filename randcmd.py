"""Module imports"""

import os
import random
import urllib

import discord
from mcstatus import MinecraftServer

import editdatabase
import databasecmd
import geolocation


class Rand():
    """Rand command class"""
    def __init__(self) -> None:
        pass

    async def main(self, ctx):
        """returns random servers out of the database"""

        player_online = 0
        tries = 0
        message = await ctx.channel.send("checking hostnames....")
        while player_online < 1:
            hostname = editdatabase.Databasemanager().get(random.randint(0, int(editdatabase
                                                                                .Databasemanager()
                                                                                .lengh())))
            try:
                server = MinecraftServer.lookup(hostname + ":25565")
                status = server.status()
                player_online = status.players.online
            except IOError:
                pass
            tries += 1
            await message.edit(content=f"looking for players ip:{hostname} " + \
                               f"| tries: {tries}")
        print(f"found server ip:{hostname} with {player_online}"+ \
              " player(s) online")

        await message.delete()

        # embed
        status = server.status()
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
        embed = discord.Embed(title="Random Server", description="motd: " +
                                 status.description, color=0xFFA500)
        embed.add_field(name="ip", value=hostname, inline=True)
        embed.add_field(name="Latency in ms", value=status.latency,
                    inline=True)
        embed.add_field(name="version", value=status.version.name,
                           inline=False)
        embed.add_field(name=f"Players online ({status.players.online})",
                           value=databasecmd.CMD().getplayernames(server),
                           inline=False)
        embed.add_field(name="Geolocation", value=geolocation.Serverlocation(hostname).main(),
                           inline=False)
        embed.set_image(url='attachment://rand.jpg')
        if img_data is not None:
            await ctx.channel.send(embed=embed, file=file)
        else:
            await ctx.channel.send(embed=embed)
