import datetime
import discord
from discord.ext import commands
from manager import Manager

class Member:
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Returns information about the image pool.")
    async def poolinfo(self, ctx):
        image_count = self.bot.db.image_count()
        image_assigned_count = self.bot.db.image_assigned_count()
        await ctx.send("There are {} images in the pool of which {:.2f}% of them have been assigned.".format(image_count, (image_assigned_count * 100) / image_count))

    @commands.command(name="gentarget", brief="Generates a target for practicing.")
    async def gen_target(self, ctx):
        target = self.bot.db.new_target(ctx.author)
        embed=discord.Embed(title="Your Target", description=target.target_id, color=0x000000)
        embed.set_footer(text="To reveal type !reveal [number]")
        await ctx.author.send(embed=embed)
    
    @commands.command(brief="Reveal a target.")
    async def reveal(self, ctx, target_id : str=None):

        if not target_id:
            await ctx.send("Target id is missing!")
            return

        target = self.bot.db.get_target(target_id)
        if target:
            if not target.revelation_date:
                target.revelation_date = datetime.datetime.now()
            target.times_revealed += 1
            target.save()

            embed=discord.Embed(title="Your target image", description="[{}]({})".format(target_id, target.image.link), color=0xffffff)
            embed.set_image(url=target.image.link)
            await ctx.author.send(embed=embed)
        else:
            await ctx.author.send("Target not found.")

    @commands.command(brief="Get information about a target number.")
    async def info(self, ctx, target_id : str=None):

        if not target_id:
            await ctx.send("Target id is missing!")
            return
        
        target = self.bot.db.get_target(target_id)
        if target:
            revelation_date = "not revealed yet"
            if target.revelation_date:
                revelation_date = target.revelation_date.strftime("%m/%d/%y %H:%M")
            embed=discord.Embed(color=0x2b0063)
            embed.add_field(name=target_id, value="Requested by: " + target.requested_by
            + "\nAssigned at: " + target.assigned_date.strftime("%m/%d/%y %H:%M")
            + "\nRevealed at: " + revelation_date
            + "\nRevealed " + str(target.times_revealed) + " times", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Target not found.")
    
def setup(bot):
    bot.add_cog(Member(bot))