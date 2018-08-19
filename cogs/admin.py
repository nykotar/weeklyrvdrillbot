import discord
from discord.ext import commands
import imgurpython
import config
from manager import Manager

class Admin():

    def __init__(self, bot):
        self.bot = bot
        self.db = Manager()
        self.imgur = imgurpython.ImgurClient(config.IMGUR_CLIENT_ID, config.IMGUR_CLIENT_SECRET)

    @commands.command()
    #@commands.has_permissions(administrador=True)
    async def refreshpool(self):
        images = self.imgur.get_album_images(config.IMGUR_ALBUM)
        print("Got images")
        msg = await self.bot.say("Refreshing..")

        await self.db.refreshpool(images)
        
        await self.bot.edit_message(msg, "Done!")
        print("Done refreshing.")

def setup(bot):
    bot.add_cog(Admin(bot))