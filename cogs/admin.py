from discord.ext import commands
import asyncio
import imgurpython
import config
from manager import Manager

class Admin:

    def __init__(self, bot):
        self.bot = bot
        self.imgur = imgurpython.ImgurClient(config.IMGUR_CLIENT_ID, config.IMGUR_CLIENT_SECRET)

    @commands.command(brief="Updates the bot's image pool database.")
    @commands.has_permissions(administrador=True)
    async def refreshpool(self, ctx):
        print("Pool refresh requested!")
        images = self.imgur.get_album_images(config.IMGUR_ALBUM)
        msg = await ctx.send("Refreshing..")
        count = await self.bot.db.add_images(images)
        await msg.edit(content="Done! %d images were added into the database." % count)
        print("Done refreshing.")

def setup(bot):
    bot.add_cog(Admin(bot))