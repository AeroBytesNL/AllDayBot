import disnake
from disnake.ext import commands
from env import *

class Introduce_remover(commands.Cog):



    def __init__(self, bot: commands.Bot):

        self.bot = bot
        print("Cog Introduce remover is loaded!")

    

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(Channel.STEL_JEZELF_VOOR)

        messages_in_channel = await channel.history(limit=1000).flatten()

        for message in messages_in_channel:
            if message.author.id == member.id:
                print(f"#stel-jezelf-voor message deleted from user {member.display_name}")
                await message.delete()
                await Introduce_remover.log_removed_introduction(self, member)



    async def log_removed_introduction(self, member):
        channel = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        embed=disnake.Embed(title="#stel-jezelf-voor bericht automatisch verwijderd van:", description=f"{member.display_name}", color=disnake.Color.red())
        await channel.send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(Introduce_remover(bot))