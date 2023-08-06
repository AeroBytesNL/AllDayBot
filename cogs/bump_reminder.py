import disnake
from disnake.ext import commands
from env import *
import time
class Bump_reminder(commands.Cog):


    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Bump reminder is loaded!")



    @commands.Cog.listener()
    async def on_message(self, message):

        # check if message is send from a bot, then do nothing
        if message.author == self.bot.user or message.author.bot:
            return

        # If bump command has executed succesfully
        if str(message.interaction.name) == "bump":
            # Start timer for 120 minutes  
            # After timer send bump remind message
            await Bump_reminder.bump_remind_embed(self)



    async def bump_remind_embed(self):

        time.sleep(7200)

        channel = self.bot.get_channel(Channel.ALLDAYBOT)
        await channel.send("Bump reminder! Er kan weer gebumped worden! Doe dit d.m.v het command `/bump`. Hierdoor wordt onze server groter!")

def setup(bot: commands.Bot):
    bot.add_cog(Bump_reminder(bot))