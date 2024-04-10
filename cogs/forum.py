import disnake
from disnake.ext import commands, tasks
from env import *
from datetime import datetime


class Forum(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Forum is loaded!")


    @commands.Cog.listener()
    async def on_ready(self):
        self.not_responding_checker.start()


    # Not responding age checker
    @tasks.loop(seconds=30)
    async def not_responding_checker(self):
        print("Scanning for forum posts that doesn't have a response....")

        channel = await self.bot.fetch_channel(Channel.TECH_SUPPORT)
        archived_threads = channel.archived_threads()

        async for archived_thread in archived_threads:                        
            if hasattr(archived_thread, "name") == []: return
            
            print(archived_thread.name)
    

    @commands.slash_command(description="Markeer dit forum kanaal als opgelost")
    async def opgelost(self, inter):
        print(f"User {inter.author.name} gebruikte het command 'opgelost'")
        valide_owner = await Forum.valide_thread_command_owner(self, inter)
        if valide_owner == True:
            await Forum.close_thread(self, inter)
        else:
            await inter.response.send_message("Whoepsiedoepsie, jij bent geen admin of eigenaar van deze thread, en mag dit dus niet doen!", ephemeral=True)
        await Forum.log_command(self, author=inter.author, command="`/opgelost`", channel=inter.channel)


    @commands.default_member_permissions(moderate_members=True)
    @commands.slash_command(description="Markeer dit forum kanaal als niet opgelost")
    async def niet_opgelost(self, inter):
        print(f"User {inter.author.name} gebruikte het command 'niet opgelost'")
        await Forum.log_command(self, author=inter.author, command="`/niet_opgelost`", channel=inter.channel)
        await Forum.not_solved_close_thread(self, inter)


    async def close_thread(self, inter):
        embed=disnake.Embed(title="Opgelost!", description=f"Ik heb deze thread als opgelost gemarkeerd! Thread is gesloten door {inter.author.mention}", color=disnake.Colour.green())
        await inter.response.send_message(embed=embed)  
        
        thread = self.bot.get_channel(inter.channel.id)
        
        tags = thread.parent.get_tag_by_name("Opgelost")
        await thread.add_tags(tags)
        await thread.edit(locked=True, archived=True)   
    

    async def not_solved_close_thread(self, inter):
        embed=disnake.Embed(title="Niet opgelost!", description=f"Ik heb deze thread als niet opgelost gemarkeerd! Thread is gesloten door {inter.author.mention}", color=disnake.Colour.red())
        await inter.response.send_message(embed=embed)  
        
        thread = self.bot.get_channel(inter.channel.id)
        
        tags = thread.parent.get_tag_by_name("Niet opgelost")
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


    # Send reminder of answering thread to owner 
    async def reminder_thread_in_dm(self, thread_name, thread_owner):

        user = await self.bot.get_or_fetch_user(thread_owner.id)
        await user.send(f"""
Beste {thread_owner.display_name}, onlangs heb je een forumpost voor tech-support geopend in All Day Tech & Gaming. Tot op heden hebben wij geen verdere reactie van jou ontvangen op de antwoorden die je hebt gekregen naar aanvang jou vraag. Middels dit bericht willen wij je graag herrineren te reageren op je forumpost. 

Als "{thread_name}" is opgelost, deel dan eventueel de oplossing met ons en gebruik het commando  `/opgelost` in de forum post om de post te sluiten.

Mocht je reactie uitblijven? Dan sluiten wij automatisch je post over 2 dagen. 

Uitgaand je voldoende geinformeerd te hebben.

Met vriendelijke groet.
Het beheer van All Day Tech & Gaming.
""")


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