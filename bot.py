import discord
from discord.ext import commands
import imgurpython
from manager import Manager
import config

imgur = imgurpython.ImgurClient(config.IMGUR_CLIENT_ID, config.IMGUR_CLIENT_SECRET)
db = Manager()
bot = commands.Bot(command_prefix=config.DISCORD_PREFIX)

@bot.event
async def on_ready():
    print('Bot ready.')

@bot.command()
async def refreshpool():
    #TODO: Check for admin rights
    images = imgur.get_album_images(config.IMGUR_ALBUM)
    print("Got images")
    msg = await bot.say("Refreshing..")

    await db.refreshpool(images)
    
    await bot.edit_message(msg, "Done!")
    print("Done refreshing.")


@bot.command(description="Returns information about the image pool.")
async def poolinfo():
    await bot.say("There are %d images in the pool." % db.poolinfo())


bot.run(config.DISCORD_TOKEN)