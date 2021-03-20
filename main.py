import discord
import os
import json
from bot import bot

with open('config.json') as f:
    creds = json.load(f)

client = discord.Client()

class handler():
    def __init__(self):
        self.bot = bot()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # add url check
    # add user check
    if message.author == client.user:
        return

    

    if message.content.startswith('!tv add'):
        await message.channel.send('Hello!')


client.run(creds['token'])