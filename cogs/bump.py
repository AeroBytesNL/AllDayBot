import disnake
from disnake.ext import commands, tasks
from env import *
import time
from datetime import datetime, timedelta, timezone
from database import Database
from helpers.error import Log

class BumpReminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_bump_time = None
        self.bump_channel_id = Channel.BUMP
        self.bump_interval = timedelta(hours=2)
        Log.info("Loaded Cog bump")

    @tasks.loop(minutes=5)
    async def check_bump(self):
        channel = self.bot.get_channel(self.bump_channel_id)
        if not channel:
            Log.error(f"Error in check_bump: Channel not found")
            return

        if self.last_bump_time:
            time_since_last_bump = datetime.now(timezone.utc) - self.last_bump_time
            if time_since_last_bump >= self.bump_interval:
                await channel.send("Reminder: It's time to bump the server!")
                self.last_bump_time = datetime.now(timezone.utc)
        else:
            self.last_bump_time = datetime.now(timezone.utc)
            await channel.send("De server kan weer gebumped worden! Dit kan d.m.v het command `/bump`. Dit helpt de server groeien!")

    @check_bump.before_loop
    async def before_check_bump(self):
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_bump.start()

def setup(bot):
    bot.add_cog(BumpReminder(bot))
