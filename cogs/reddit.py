import discord
from discord.ext import commands
import asyncio
import schedule
import praw
import config
from manager import Manager

class Reddit:

    def __init__(self, bot):
        self.bot = bot
        self.db = Manager()
        self.reddit = praw.Reddit(client_id=config.REDDIT_CLIENT_ID,
                     client_secret=config.REDDIT_CLIENT_SECRET, password=config.REDDIT_PASSWORD,
                     user_agent=config.REDDIT_USER_AGENT, username=config.REDDIT_USERNAME)
        schedule.every(10).seconds.do(self.run_drill)
        self.bot.loop.create_task(self.run_tasks())

    def run_drill(self):
        print("sending post")
        self.reddit.subreddit('nykotest').submit(title="Weekly Remote Viewing Challenge: XXXX"
        , selftext="Target Reference Number: {}\nThis post was submitted by the bot.".format(self.db.new_target(self.bot.user)))
        print("sent")

    async def run_tasks(self):
        while not self.bot.is_closed:
            schedule.run_pending()
            await asyncio.sleep(5)

def setup(bot):
    return
    bot.add_cog(Reddit(bot))