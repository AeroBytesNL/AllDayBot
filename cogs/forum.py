import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
from env import *

class Forum(commands.Cog):

    
    def __init__(self, bot: commands.Bot):

        self.bot = bot
        print("Cog Forum is loaded!")



    @commands.slash_command(description="Markeer dit forum kanaal als opgelost")
    async def opgelost(self, inter):
            
            print(f"User {inter.author.name} gebruikte het command 'opgelost'")
            valide_owner = await Forum.valide_thread_command_owner(self, inter)
            if valide_owner == True:
                await Forum.close_thread(self, inter)
            else:
                await inter.response.send_message("Whoepsiedoepsie, jij bent geen admin of eigenaar van deze thread, en mag dit dus niet doen!", ephemeral=True)
            await Forum.log_command(self, author=inter.author, command="`/opgelost`", channel=inter.channel)



    async def close_thread(self, inter):

        embed=disnake.Embed(title="Opgelost!", description=f"Ik heb deze thread als opgelost gemarkeerd! Thread is gesloten door {inter.author.mention}", color=0xdf8cfe)
        await inter.response.send_message(embed=embed)  
        
        thread = self.bot.get_channel(inter.channel.id)
        
        tags = thread.parent.get_tag_by_name("Opgelost")
        await thread.add_tags(tags)
        await thread.edit(locked=True, archived=True)   
    


    async def valide_thread_command_owner(self, inter):

        guild = await self.bot.fetch_guild(env_variable.GUILD_ID) 
        role_list = [guild.get_role(Management_roles.OPRICHTER_ID), guild.get_role(Management_roles.ADMINISTRATOR), guild.get_role(Management_roles.SERVER_DEVELOPER), guild.get_role(Management_roles.MODERATOR)]

        if inter.author.id == inter.channel.owner_id:
            return True
        
        i = 0
        for role in role_list:
            if role in inter.author.roles:
                i = 1

        if i != 0:
            return True
        else:
            return False



    # Command logging
    async def log_command(self, author, command, channel):

        embed=disnake.Embed(title=f"Een user heeft een command gebruikt!", description=f"\n", color=disnake.Color.green())
        embed.add_field(name="Command::", value=str(command), inline=True)
        embed.add_field(name="Author:", value=str(author.mention), inline=True)
        embed.add_field(name="Kanaal:", value=str(channel.mention), inline=False)
        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        await channel_to_send.send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(Forum(bot))