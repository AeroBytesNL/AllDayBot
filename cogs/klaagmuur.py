import disnake
from disnake.ext import commands, tasks


class Klaagmuur(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Klaagmuur is loaded!")




def setup(bot: commands.Bot):
    bot.add_cog(Klaagmuur(bot))