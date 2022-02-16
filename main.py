from turtle import right
import discord
from discord.ext import commands
import authenticator
from discord.utils import get

cogs = [authenticator]

client = commands.Bot(command_prefix='-')

@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="-help"), status=discord.Status.do_not_disturb)
    print('Ready!\n')

@client.event
async def on_reaction(reaction, user):
    print(f"added reaction {reaction.emoji}")
    if user != client.user:
        if reaction.emoji == "⬅️":
            print("left")
        if reaction.emoji == "➡️":
            print("right")

for i in range(len(cogs)):
    cogs[i].setup(client)

client.run('OTQxNjI2NTMzMDc5MDUyMzE4.YgYsDA.qc3w5Veg5X0VepS1-iEIXkqWW18')