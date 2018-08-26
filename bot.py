from os import listdir
from os.path import isfile, join
import discord
from discord.ext import commands
from manager import Manager
import config


class IngoBot(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        print("Loading database..")
        self.db = Manager()

        print("Loading extensions..")
        cogs = [f.replace('.py', '') for f in listdir(config.COGS_DIR) if isfile(join(config.COGS_DIR, f))]
        for extension in cogs:
            try:
                bot.load_extension(config.COGS_DIR + "." + extension)
                print("Loaded", extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))  

    
    async def on_ready(self):
        print('Bot ready.')


bot = IngoBot(command_prefix=config.DISCORD_PREFIX)
bot.run(config.DISCORD_TOKEN)