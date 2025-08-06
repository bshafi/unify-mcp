import discord
import asyncio
import dotenv

dotenv.load_dotenv()

import os

import multiprocessing
import os
from multiprocessing import Process, Queue

def run_discord_bot(handle_message):
    import discord

    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    intents.message_content = True

    class MyClient(discord.Client):
        async def on_ready(self):
            print(f"Connected as {self.user}")
            for guild in self.guilds:
                print(f"In server: {guild.name} (ID: {guild.id})")

            channel = self.get_channel(int(os.environ['GENERAL_CHANNEL_ID']))
            if not channel:
                print("Channel not found.")
                await self.close()

        async def on_message(self, message):
            await handle_message(message)

    TOKEN = os.environ['DISCORD_TOKEN']
    client = MyClient(intents=intents)
    client.run(TOKEN)
