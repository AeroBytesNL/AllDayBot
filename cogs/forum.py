import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
from env import *

class forum(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        @bot.slash_command(description="Markeer dit forum kanaal als opgelost")
        async def opgelost(inter):
                print(f"User {inter.author.name} gebruikte het command 'opgelost'")
                valide_owner = await valide_thread_command_owner(inter)
                if valide_owner == True:
                    await close_thread(inter)
                else:
                    await inter.response.send_message("Whoepsiedoepsie, jij bent geen admin of eigenaar van deze thread, en mag dit dus niet doen!", ephemeral=True)
                await log_command(author=inter.author, command="`/opgelost`", channel=inter.channel)

        async def close_thread(inter):

            get_channel_id = inter.channel.id         

            embed=disnake.Embed(title="Opgelost!", description=f"Ik heb deze thread als opgelost gemarkeerd! Thread is gesloten door {inter.author.mention}", color=0xdf8cfe)
            await inter.response.send_message(embed=embed)  
            
            thread = bot.get_channel(inter.channel.id)
            
            tags = thread.parent.get_tag_by_name("Opgelost")
            await thread.add_tags(tags)
            await thread.edit(locked=True, archived=True)   
        

        async def valide_thread_command_owner(inter):
            guild = await bot.fetch_guild(env_variable.GUILD_ID) # CHANGE THIS TO ADTG BEFORE COMMIT TODO
            role_list = [guild.get_role(889830873246105630), guild.get_role(723888611979690046)]

            count_roles_not_in = 0
            for role in role_list:
                if role not in inter.author.roles:
                    count_roles_not_in = count_roles_not_in + 1

            if count_roles_not_in == 2:
                if inter.author.id == inter.channel.owner_id:
                    return True
                else:
                    return False

            elif count_roles_not_in == 0 or 1:
                return True        


        # Command logging
        async def log_command(author, command, channel):

            embed=disnake.Embed(title=f"Een user heeft een command gebruikt!", description=f"\n", color=disnake.Color.green())
            embed.add_field(name="Command::", value=str(command), inline=True)
            embed.add_field(name="Author:", value=str(author.mention), inline=True)
            embed.add_field(name="Kanaal:", value=str(channel.mention), inline=False)
            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await channel_to_send.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(forum(bot))