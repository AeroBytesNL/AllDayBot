import disnake
from disnake.ext import commands
from env import *
import random

class Custom_welcome_msg(commands.Cog):

    

    def __init__(self, bot: commands.Bot):

        self.bot = bot
        self.just_joined_members = []
        self.funny_sentences = ["Heb je pils mee genomen?", "Jah keal, hoop dat je blij bent om hier te zijn.", "He hoo", "HA je moeeeeder"]
        print("Cog Custom welcome message is loaded!")



    @commands.Cog.listener()
    async def on_member_join(self, member):

        self.just_joined_members.append(int(member.id))



    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        # If member needed verification, and has done it, and user is in just joined members list
        if before.pending == True and after.pending == False and before.id in self.just_joined_members:

            channel = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            guild = await self.bot.fetch_guild(env_variable.GUILD_ID)

            embed=disnake.Embed(title=f"Er is een lid op onze server bijgekomen!", description=f"Welkom {before.mention}!", color=disnake.Color.green())
            embed.add_field(name=str(random.choice(self.funny_sentences)), value="\n", inline=False)
            embed.set_thumbnail(url=guild.icon)
            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await channel_to_send.send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(Custom_welcome_msg(bot))