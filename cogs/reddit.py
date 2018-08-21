import discord
from discord.ext import commands
import asyncio
import datetime
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
        schedule.every(20).seconds.do(self.run_drill)
        self.bot.loop.create_task(self.run_tasks())

    def run_drill(self):
        print("sending post")
        last_drill = self.db.get_last_drill()
        if last_drill != None and not last_drill.revealed:
            print("editing")
            post = self.reddit.submission(id=last_drill.post_id)
            post.edit(post.selftext + "\nTarget: " + last_drill.target.image.link)
            last_drill.revealed = True
            last_drill.save()

        target = self.db.new_target(self.bot.user)
        title = "Weekly Remote Viewing Challenge: " + datetime.date.today().strftime("%A %B %d, %Y") 
        message = "Target Reference Number: {}  \nThis post was submitted by the bot.  ".format(target.target_id)
        post_id = self.reddit.subreddit('nykotest').submit(title=title,
            selftext=message,
            send_replies=False)
        self.db.new_drill(target, post_id)
        
        print("sent")

    async def run_tasks(self):
        while not self.bot.is_closed:
            schedule.run_pending()
            await asyncio.sleep(5)

def setup(bot):
    bot.add_cog(Reddit(bot))