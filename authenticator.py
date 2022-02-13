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
                hostname = editdatabase.Databasemanager().get(random.randint(0, int(editdatabase.Databasemanager().lengh())))
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
                    file = discord.File("image.jpg") 

                            
            """embed for displaying infos"""

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

        elif message == "all-players":
            server_id = 1
            ips = {}
            sorted_dict = {}
            key_arr = []
            listvalue = 0
            #int(editdatabase.Databasemanager().lengh()
            while (server_id < 50):
                hostname = editdatabase.Databasemanager().get(server_id)
                try:
                    server = MinecraftServer.lookup(hostname + ":25565")
                    status = server.status()
                except:
                    pass

                if(int(status.players.online) > 0):
                    ips[f"{hostname},{status.version.name}"] = status.players.online
                server_id += 1

            sorted_keys = sorted(ips, key=ips.get, reverse=True)
            for w in sorted_keys:
                sorted_dict[w] = ips[w]

            for key in sorted_dict.keys():
                key_arr.append(key)
            
            await ctx.channel.send(f"{listvalue + 1}. IP: {key_arr[listvalue].split(',')[0]} | version: {key_arr[listvalue].split(',')[1]} | players: {sorted_dict[key_arr[listvalue]]}")


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