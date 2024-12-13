import disnake
from disnake.ext import commands
from env import Channel, env_variable

class Showcase_remover(commands.Cog):
    def  __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog showcase_remover is loaded!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        showcase_channel = self.bot.get_channel(Channel.SHOWCASE)
        log_channel = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)

        all_messages = await showcase_channel.history(limit=2000).flatten()

        for message in all_messages:
            if message.author.id != member.id: return

            await message.delete()
            await Showcase_remover.log_removed_showcase(self, member, channel=log_channel)

    async def log_removed_showcase(self, member, channel):
        embed=disnake.Embed(title="#showcase bericht automatisch verwijderd van:", description=f"{member.display_name}", color=disnake.Color.red())
        await channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Showcase_remover(bot))