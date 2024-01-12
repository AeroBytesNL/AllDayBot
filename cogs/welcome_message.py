import disnake
from disnake.ext import commands
from env import Channel


class Welcome_message(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Welcome_message is loaded!")
        self.joined_members = []


    @commands.Cog.listener() 
    async def on_member_join(self, member):
        self.joined_members.append(member.id)


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.pending != True and after.pending != False:
            return
        
        if before.id not in self.joined_members:
            return 
        
        self.joined_members.remove(before.id)
        
        general_channel = await self.bot.fetch_channel(Channel.GENERAL)
        joined_user = await self.bot.get_or_fetch_user(before.id)
        bot_user = await self.bot.get_or_fetch_user(self.bot.user.id)

        await general_channel.send(f"Welkom {joined_user} in All Day Tech & Gaming.\n\nIn onze server maken we gebruik van verschillende kanalen om onderwerpen gescheiden te houden:\n- Hulp nodig met tech? <#1019678705045471272>\n- Voor tech gesprekken zie <#723556858820034612>\n- Voor game gesprekken zie <#759456512165937183>\nMocht je vragen hebben m.b.t het beheer dan kun je {bot_user.mention} DM'en!")


def setup(bot: commands.Bot):
    bot.add_cog(Welcome_message(bot))