import discord
import os
import json
from bot import bot
import pandas as pd
import csv
import random
import re

with open('config.json') as f:
    creds = json.load(f)



class handler():
    def __init__(self):
        self.bot = bot()
        self.videoList = list(pd.read_csv('videoList.csv'))

    
    def receive(self, message):
        if message.content.startswith('$vault add'):
            name = str(message.author).split('#')[0]
            url = message.content.split("add",1)[1]
            m = re.search(r"[a-zA-Z0-9_-]{11}$", str(message.content))
            if m and 'watch?v=' in url:
                self.add_video(message, url)
                return f'Thanks {name}, that shit has been added to the vault'
            else:
                return f'Hey {name}, you shitbag, make sure the video you enter is legit'
            #url check
            
        elif message.content.startswith('$vault random'):
            return self.random_video()

    def add_video(self, message, url):
        self.videoList.append(url)
        with open('videoList.csv','a') as fd:
            fd.write(url)
        #add success or failure
        

    def random_video(self):
        return random.choice(self.videoList)

    def delete_video(self):
        pass


client = discord.Client()
handler = handler()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # add url check
    # add user check
    if message.author == client.user:
        return

    resp = handler.receive(message)

    await message.channel.send(resp)

    # if message.content.startswith('!tv add'):
    #     await message.channel.send('Hello!')


client.run(creds['token'])