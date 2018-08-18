import discord
from discord.ext import commands
import config

bot = commands.Bot(command_prefix=config.DISCORD_PREFIX)

@bot.event
async def on_ready():
    print('Bot ready.')


bot.run(config.DISCORD_TOKEN)