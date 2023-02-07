import os
import discord
from discord.ext import commands

# from dotenv import load_dotenv
# load_dotenv()

from revChatGPT.Official import AsyncChatbot
gpt = AsyncChatbot(api_key=os.environ["OPENAI_API_KEY"])

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='', intents=intents)


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
        loading_message = await message.channel.send('```json\n"ChatGPT is generating a response....."\n```')#, reference=message)
        data = await gpt.ask(message.content)
        res = data["choices"][0]["text"]
        # if res[0] == " ":
            # res = res[1:]
        res = res.lstrip()
        await loading_message.delete()
        if (len(res) > 1900):
            chunks = [res[i:i+1900] for i in range(0, len(res), 1900)]
            for chunk in chunks:
                await message.channel.send(quotes + chunk + quotes)
                # await message.channel.send(chunk)
        else:
            await message.channel.send(quotes + res + quotes)
            # await message.channel.send(res)

bot.run(os.environ["DISCORD_TOKEN"])
