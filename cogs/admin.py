from discord.ext import commands
import asyncio
import imgurpython
import config
from manager import Manager

class Admin:

    def __init__(self, bot):
        self.bot = bot
        self.db = Manager()
        self.imgur = imgurpython.ImgurClient(config.IMGUR_CLIENT_ID, config.IMGUR_CLIENT_SECRET)

    @commands.command(brief="Updates the bot's image pool database.")
    @commands.has_permissions(administrador=True)
    async def refreshpool(self):
        print("Pool refresh requested!")
        images = self.imgur.get_album_images(config.IMGUR_ALBUM)
        msg = await self.bot.say("Refreshing..")

        count = await self.db.add_images(images)
        
        await self.bot.edit_message(msg, "Done! %d images were added into the database." % count)
        print("Done refreshing.")

def setup(bot):
    bot.add_cog(Admin(bot))