import discord
from discord.ext import commands
from manager import Manager

class Member:
    
    def __init__(self, bot):
        self.bot = bot
        self.db = Manager()

    @commands.command(brief="Returns information about the image pool.")
    async def poolinfo(self):
        await self.bot.say("There are %d images in the pool." % self.db.poolinfo())

    @commands.command(name="gentarget", brief="Generates a target for practicing.", pass_context=True)
    async def gen_target(self, ctx):
        number = self.db.new_target(ctx.message.author)
        embed=discord.Embed(title="Your Target", description=number, color=0x000000)
        embed.set_footer(text="To reveal type !reveal [number]")
        await self.bot.whisper(embed=embed)
    
    @commands.command(brief="Reveal a target.")
    async def reveal(self, target_id : str=None):

        if not target_id:
            await self.bot.say("Target id is missing!")
            return

        target = self.db.get_target(target_id)
        if target:
            embed=discord.Embed(title="Your target image", description=target_id, color=0xffffff)
            embed.set_thumbnail(url=target.image.link)
            await self.bot.whisper(embed=embed)
            #await self.bot.whisper(target.image.link)
        else:
            await self.bot.whisper("Target not found.")
    
def setup(bot):
    bot.add_cog(Member(bot))