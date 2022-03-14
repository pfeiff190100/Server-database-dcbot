import discord, urllib

class embedprint():
    def __init__(self) -> None:
        pass

    async def ri_embed(self, ctx, status, hostname):
        """embed for rand and info command command"""

        # gets the favicon of the minecraft server
        img_data = status.favicon
        if img_data is not None:
            response = urllib.request.urlopen(img_data)
            with open('pics/rand.jpg', 'wb') as file:
                file.write(response.file.read())
                file = discord.File("pics/rand.jpg", filename="rand.jpg")

        # embed for displaying infos

        embed = discord.Embed(title="Server", description="motd: " +
                                 status.description, color=0xff6ec7)
        embed.add_field(name="ip", value=hostname, inline=False)
        embed.add_field(name="version", value=status.version.name,
                           inline=False)
        embed.add_field(name="Players online", value=status.players.online,
                           inline=False)
        embed.add_field(name="Latency in ms", value=status.latency,
                           inline=False)
        embed.set_image(url='attachment://rand.jpg')
        if img_data is not None:
            await ctx.channel.send(embed=embed, file=file)
        else:
            await ctx.channel.send(embed=embed)
