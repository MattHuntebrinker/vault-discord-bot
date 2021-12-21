import discord
import os
import json

from pymysql.cursors import Cursor
from bot import bot
import pandas as pd
import csv
import random
import pymysql
import re



# FUTURE HIT YOUTUBE API AND GET VIDEO DETAILS


class handler():
    def __init__(self):
        with open('config.json') as f:
            self.creds = json.load(f)
        self.token = self.creds['token']

        self.bot = bot()
        self.db = pymysql.connect(host=self.creds['endpoint'], user=self.creds['user'], password=self.creds['db_pass'])
        self.cursor = self.db.cursor()
        self.cursor.execute('''select now()''')
        print(self.cursor.fetchall())
        self.cursor.execute('''use vault_db''')
        print(self.cursor.fetchall())
        self.cursor.execute('''show tables''')
        print(self.cursor.fetchall())
        self.cursor.execute('''select * from vault_db.vault''')
        print(self.cursor.fetchall())



    
    def receive(self, message):
        if message.content.startswith('$vault add'):
            name = str(message.author).split('#')[0]
            url = message.content.split("add",1)[1]
            m = re.search(r"[a-zA-Z0-9_-]{11}$", str(message.content))
            if m and 'watch?v=' in url:
                self.add_video(url, name)
                return f'Thanks {name}, that shit has been added to the vault'
            else:
                return f'Hey {name}, you shitbag, make sure the video you enter is legit'
            #url check
            
        elif message.content.startswith('$vault random'):
            return self.random_video()

    def add_video(self, url, name):
        self.cursor.execute("INSERT IGNORE INTO vault(url) VALUES('{0}')".format(url.strip()))
        print(self.cursor.fetchall())
        self.db.commit()
        
        #add success or failure
        

    def random_video(self):
        query = '''select distinct url from vault_db.vault'''
        sql_response = pd.read_sql(query, self.db)
        url_list = sql_response['url'].tolist()
        print(sql_response['url'].tolist())
        return random.choice(url_list)

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


client.run(handler.token)