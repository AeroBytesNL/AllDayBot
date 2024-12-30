from disnake.ext import commands, tasks
from env import *
from database import Database
from helpers.error import Log

class InviteTracker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Loaded Cog Invite tracker")


def setup(bot: commands.Bot):
    bot.add_cog(InviteTracker(bot))
