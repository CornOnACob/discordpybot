import os
import discord
from discord.ext import commands

from revChatGPT.Official import AsyncChatbot
gpt = AsyncChatbot(api_key=os.environ["OPENAI_API_KEY"])

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='', intents=intents)

def split_string(input_string):
    split_strings = []
    start = 0
    while start < len(input_string):
        end = start + 1900
        if end < len(input_string):
            while input_string[end] != ' ':
                end -= 1
        split_strings.append(input_string[start:end])
        start = end + 1
    return split_strings

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.name.startswith('chatgpt'):
        quotes = ""
        if message.channel.name == 'chatgpt':
            quotes = "```"
        loading_message = await message.channel.send('```json\n"ChatGPT is generating a response....."\n```')
        try:
            data = await gpt.ask(message.content)
            res = data["choices"][0]["text"]
            res = res.lstrip()
            await loading_message.delete()
            if (len(res) > 1900):
                chunks1 = [res[i:i+1900] for i in range(0, len(res), 1900)]
                chunks = split_string(res)
                for chunk in chunks:
                    await message.channel.send(quotes + chunk + quotes)
            else:
                await message.channel.send(quotes + res + quotes)
        except Exception as e:
            await message.channel.send("```An error has occured.. Try again or contact Michael```")
            print("An error occurred:", e)

bot.run(os.environ["DISCORD_TOKEN"])
