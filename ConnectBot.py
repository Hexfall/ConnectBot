import asyncio
import time

import discord

class ConnectBot(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
    
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
    