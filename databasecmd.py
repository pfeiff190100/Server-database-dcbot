import discord, random, urllib, time
from mcstatus import MinecraftServer
from threading import Thread
import editdatabase, serverlookup
class CMD():
    def __init__(self) -> None:
        self.data = []

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
    
    async def searchservers(self, ctx):
        page = 0
        counter = 0
        pagelengh = 0
        out = ""
        outadresses = []
        host_count = 1
        threadlengh = 10
        #int(editdatabase.Databasemanager().lengh())
        while host_count < 1000:
            while self.threadcounter > 100:
                time.sleep(0.1)
            outadresses.append(editdatabase.Databasemanager().get(host_count))
            if len(outadresses) >= threadlengh:
                lookup = serverlookup.Ping(threadlengh, outadresses.copy(), self)
                Thread(target=lookup.main).start()
                self.threadcounter += 1
                outadresses.clear()
            host_count += 1
        print(self.data)
            
        self.data.sort(key=lambda x:x[2], reverse=True)
        counter = page * 5
        """embed for displaying infos"""
        embedVar = discord.Embed(title="Servers", description="A list of servers with players online", color=0xFF7373)
        while(counter < len(self.data) and pagelengh < 10):
            out += f"{counter + 1}. IP: {self.data[counter][0]} | version: {self.data[counter][1]} | players: {self.data[counter][2]} \n"
            counter += 1
            pagelengh += 1
        embedVar.add_field(name=f"Page: {page + 1}", value=out ,inline=False)
        msg = await ctx.channel.send(embed=embedVar)   
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

    async def checkreaction(self, reaction, user):
        if str(reaction.emoji) == "⬅️":
            print("page left")
        if str(reaction.emoji) == "➡️":
            print("page right")
