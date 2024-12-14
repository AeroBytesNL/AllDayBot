import disnake
from disnake.ext import commands
from helpers.error import Log

class Website(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Loaded Cog website")

    @commands.slash_command()
    async def website(self, inter):
        pass

    @website.sub_command(description="Krijg de URL van de ADT&G site!")
    async def url(self, inter):
        await inter.response.send_message("https://alldaytechandgaming.nl/", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Website(bot))