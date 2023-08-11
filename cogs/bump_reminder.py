import disnake
from disnake.ext import commands, tasks
from env import *
import time
from datetime import datetime, timedelta

class Bump_reminder(commands.Cog):


    
    def __init__(self, bot: commands.Bot):

        self.bot = bot
        print("Cog Bump reminder is loaded!")
        self.last_processed_bump = 0


    @commands.Cog.listener()
    async def on_ready(self):

        Bump_reminder.check_if_bump_is_ready.start(self)



    @tasks.loop(seconds=5)
    async def check_if_bump_is_ready(self):

        # Get the bot channel
        channel = self.bot.get_channel(Channel.ALLDAYBOT)

        # Find the last bump
        messages = list(
        filter(
            lambda x: x.interaction is not None and x.interaction.name == "bump", 
            await channel.history(limit=50).flatten()
        )
        )
        last_bump = max(messages, key=lambda x: x.id)

        # Check if we've already processed this bump
        if last_bump.id == self.last_processed_bump: return

        # Check if the last bump happened more than 2 hours ago
        bump_time = datetime.fromtimestamp((last_bump.id >> 22) + 1420070400000)
        diff = int((datetime.now() - bump_time).seconds)

        if diff > 7200: return

        # Send the reminder
        #await channel.send("De server kan weer gebumped worden! Dit kan d.m.v het command `/bump`. Dit helpt de server groeien!")
        print("Server ready to be bumped")
        self.last_processed_bump = last_bump.id
    

def setup(bot: commands.Bot):
    bot.add_cog(Bump_reminder(bot))