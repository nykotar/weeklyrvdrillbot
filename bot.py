from os import listdir
from os.path import isfile, join
import discord
from discord.ext import commands
from manager import Manager
import config

db = Manager()
bot = commands.Bot(command_prefix=config.DISCORD_PREFIX)

@bot.event
async def on_ready():
    print('Bot ready.')

@bot.command(brief="Returns information about the image pool.")
async def poolinfo():
    await bot.say("There are %d images in the pool." % db.poolinfo())

if __name__ == "__main__":
    print("Checking database..")
    db.load()

    print("Loading extensions..")
    cogs = [f.replace('.py', '') for f in listdir(config.COGS_DIR) if isfile(join(config.COGS_DIR, f))]
    for extension in cogs:
        try:
            bot.load_extension(config.COGS_DIR + "." + extension)
            print("Loaded", extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(config.DISCORD_TOKEN)