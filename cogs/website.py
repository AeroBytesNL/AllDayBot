import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database



class Website(commands.Cog):



    def __init__(self, bot: commands.Bot):

        self.bot = bot
        print("Cog Website is loaded!")



    @commands.slash_command()
    async def website(self, inter):
        pass



    @website.sub_command(description="Krijg de URL van de ADT&G site!")
    async def url(self, inter):
        await inter.response.send_message("https://alldaytechandgaming.nl/", ephemeral=True)
        


def setup(bot: commands.Bot):
    bot.add_cog(Website(bot))   