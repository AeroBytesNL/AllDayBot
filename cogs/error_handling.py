import disnake
from disnake.ext import commands

class ErrorHandling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Error handling is loaded!")

def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandling(bot))
