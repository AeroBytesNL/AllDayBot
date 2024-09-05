import disnake
from disnake.ext import commands
from env import *

class AntiBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog anti_bot is loaded!")


def setup(bot: commands.Bot):
    bot.add_cog(AntiBot(bot))