import discord, random, urllib
import editdatabase
from mcstatus import MinecraftServer
from discord.ext import commands


class authenticate(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def list (self, ctx, message=""):
        if (message == "rand"):
            player_online = 0
            tries = 0
            message = await ctx.channel.send("checking hostnames....")
            while(player_online < 1):
                hostname = editdatabase.Databasemanager(random.randint(0, int(editdatabase.Databasemanager(2).lengh()))).get()
                try:
                    server = MinecraftServer.lookup(hostname + ":25565")
                    status = server.status()
                    player_online = status.players.online
                except:
                    pass    
                tries += 1  
                await message.edit(content=f"looking for players ip:{hostname} tries: {tries}")   
                print(f"looking for players ip:{hostname} tries: {tries} ", end="\r") 
            
            await message.delete()
            """gets the favicon of the minecraft server"""
            img_data = status.favicon
            if(img_data != None):
                response = urllib.request.urlopen(img_data)
                with open('image.jpg', 'wb') as f:
                    f.write(response.file.read())    
                print("success")
            else:
                print("None")
                            
            """embed for displaying infos"""
            file = discord.File("image.jpg")

            embedVar = discord.Embed(title="Server", description="motd: " + status.description, color=0xff6ec7)
            embedVar.set_image(url='attachment://image.jpg')
            embedVar.add_field(name="ip", value=hostname, inline=False)
            embedVar.add_field(name="version", value=status.version.name, inline=False)
            embedVar.add_field(name="Players online", value=status.players.online, inline=False)
            embedVar.add_field(name="Latency in ms", value=status.latency, inline=False)
            if img_data != None:
                await ctx.channel.send(embed=embedVar, file= file)
            else:
                await ctx.channel.send(embed=embedVar)

        elif message == "list-online":
            pass

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