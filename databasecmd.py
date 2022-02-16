import discord, random, urllib
from mcstatus import MinecraftServer
from threading import Thread
import editdatabase
class CMD():
    def __init__(self) -> None:
        pass

    async def getrandserver(ctx):
        player_online = 0
        tries = 0
        message = await ctx.channel.send("checking hostnames....")
        while(player_online < 1):
            hostname = editdatabase.Databasemanager().get(random.randint(0, int(editdatabase.Databasemanager().lengh())))
            try:
                server = MinecraftServer.lookup(hostname + ":25565")
                status = server.status()
                player_online = status.players.online
            except:
                pass    
            tries += 1  
            await message.edit(content=f"looking for players ip:{hostname} tries: {tries}")   
        print(f"found server ip:{hostname} with {player_online} player(s) online")
        
        await message.delete()
        """gets the favicon of the minecraft server"""
        img_data = status.favicon
        if(img_data != None):
            response = urllib.request.urlopen(img_data)
            with open('image.jpg', 'wb') as f:
                f.write(response.file.read())   
                file = discord.File("image.jpg")        
        
        """embed for displaying infos"""
        embedVar = discord.Embed(title="Server", description="motd: " + status.description, color=0xff6ec7)
        embedVar.add_field(name="ip", value=hostname, inline=False)
        embedVar.add_field(name="version", value=status.version.name, inline=False)
        embedVar.add_field(name="Players online", value=status.players.online, inline=False)
        embedVar.add_field(name="Latency in ms", value=status.latency, inline=False)
        embedVar.set_image(url='attachment://image.jpg')
        if img_data != None:
            await ctx.channel.send(embed=embedVar, file= file)
        else:
            await ctx.channel.send(embed=embedVar)
