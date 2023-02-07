# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands

# from dotenv import load_dotenv
# load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='', intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def knock(ctx):
    await ctx.send('who is there')

@bot.command()
async def hello(ctx):
    await ctx.send("Choo choo! 🚅")

@bot.event
async def on_message(message):
    if message.content == 'sl' and message.channel.name == 'bot':
        await message.channel.send('🚅')

bot.run(os.environ["DISCORD_TOKEN"])
