import disnake
from disnake.ext import commands
from env import Channel

class Welcome_message(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Welcome_message is loaded!")
        self.joined_members = []
        self.potential_messages_deletion = {}

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

        welcome_message = await general_channel.send(f"Welkom {joined_user.mention} in All Day Tech & Gaming!\n\nIn onze server maken we gebruik van verschillende kanalen om onderwerpen gescheiden te houden:\n- Ben je opzoek naar hulp, dan kan je in <#1019678705045471272> een forum bericht starten.\n- Babbelen over alles wat met tech te maken heeft? <#723556858820034612>\n- Gesprekken met betrekking tot games? <#759456512165937183>\nMocht je vragen hebben m.b.t. het beheer dan kun je {self.bot.user.mention} DM'en!")
        self.potential_messages_deletion.update({before.id:welcome_message.id})
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            message_to_delete = self.bot.get_message(int(self.potential_messages_deletion[member.id]))
            await message_to_delete.delete()
            self.potential_messages_deletion.pop(member.id)
        except Exception as error:
            print("Error inside welcome_message: ", error)
            pass

def setup(bot: commands.Bot):
    bot.add_cog(Welcome_message(bot))