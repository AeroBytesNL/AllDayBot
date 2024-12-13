from disnake.ext import commands

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Status is loaded!")

    @commands.slash_command()
    async def status(self, inter):
        pass

    @status.sub_command(description="Zie de status van AllDayBot")
    async def alldaybot(self, inter):
        await inter.response.send_message("bliep bloop")

def setup(bot: commands.Bot):
    bot.add_cog(Status(bot))
