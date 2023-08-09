import disnake
from disnake.ext import commands, tasks
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



def setup(bot: commands.Bot):
    bot.add_cog(Introduce_remover(bot))