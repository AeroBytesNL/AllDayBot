import disnake
from disnake.ext import commands, tasks
from disnake.enums import ButtonStyle
from env import *
from database import Database
from mcstatus import JavaServer


class minecraft(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # Main birthday command
    @commands.slash_command()
    async def minecraft(self, inter):
        pass


    @minecraft.sub_command(description="Zie onze server info")
    async def server_informatie(self, inter):
        server = JavaServer.lookup("play.alldaytechandgaming.nl")
        status = server.status()
        print(status.players.online, status.latency, status.description, status.players.max)
        await inter.response.send_message(f"Online: {status.players.online}, latency: {status.latency}, desc: {status.description}, max spelers: {status.players.max}")


def setup(bot: commands.Bot):
    bot.add_cog(minecraft(bot))                    
