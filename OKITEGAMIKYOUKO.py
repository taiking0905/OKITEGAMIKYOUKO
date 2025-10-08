import discord
import os
import sys
from discord.ext import commands

DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.purge(limit=100)
        print("メッセージ削除完了！")
    await bot.close()
    sys.exit(0)

bot.run(DISCORD_TOKEN)
