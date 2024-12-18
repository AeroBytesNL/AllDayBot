import disnake
from disnake.ext import commands, tasks
from env import *
from datetime import datetime, date
import time
from helpers.error import Log

class buy_sell(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        buy_sell.archived_threads.start(self)
        Log.info("Loaded Cog buy_sell")


    # Selled command
    @commands.slash_command(description="Verwijder je verkochte artikel")
    async def verkocht(self, inter):
        guild = await self.bot.fetch_guild(env_variable.GUILD_ID) 
        role_list = [guild.get_role(Management_roles.OPRICHTER_ID), guild.get_role(Management_roles.ADMINISTRATOR), guild.get_role(Management_roles.SERVER_DEVELOPER), guild.get_role(Management_roles.MODERATOR)]

        if inter.author.id != inter.channel.owner_id:
            await inter.response.send_message(f"Missende rechten!", ephemeral=True)
            return
        
        i = 0
        for role in role_list:
            if role in inter.author.roles:
                i = 1

        if i == 0:
            await inter.response.send_message(f"Missende rechten!", ephemeral=True)
            return 
                
        thread = self.bot.get_channel(inter.channel.id)
        await inter.response.send_message("Ik verwijder zo de thread!", ephemeral=True)
        time.sleep(5)
        await thread.delete()   
    

    # Not selled command
    @commands.slash_command(description="Verwijder je niet verkochte artikel")
    async def niet_verkocht(self, inter):
        guild = await self.bot.fetch_guild(env_variable.GUILD_ID) 
        role_list = [guild.get_role(Management_roles.OPRICHTER_ID), guild.get_role(Management_roles.ADMINISTRATOR), guild.get_role(Management_roles.SERVER_DEVELOPER), guild.get_role(Management_roles.MODERATOR)]

        if inter.author.id != inter.channel.owner_id:
            await inter.response.send_message(f"Missende rechten!", ephemeral=True)
            return
        
        i = 0
        for role in role_list:
            if role in inter.author.roles:
                i = 1

        if i == 0:
            await inter.response.send_message(f"Missende rechten!", ephemeral=True)
            return 
                
        thread = self.bot.get_channel(inter.channel.id)
        await inter.response.send_message("Ik verwijder zo de thread!", ephemeral=True)
        time.sleep(5)
        await thread.delete()   


    @tasks.loop(seconds=15)
    async def archived_threads(self):
        try:
            channel = await self.bot.fetch_channel(Channel.BUY_SELL_FORUM)
            archived_threads = channel.archived_threads()

            async for archived_thread in archived_threads:
                if archived_thread.parent_id != Channel.BUY_SELL_FORUM:
                    return
                
                if archived_thread.archived == False:
                    return
                
                i = str(archived_thread.created_at).split(" ")[0]
                splitted_string_datetime = str(i).split("-")

                date_thread = date(int(splitted_string_datetime[0]), int(splitted_string_datetime[1]), int(splitted_string_datetime[2]))
                todays_date = date.today()
                delta = todays_date - date_thread
                
                if delta.days > 30:
                    await archived_thread.delete()
                    print("Archived thread deleted")

        except Exception as error:
            print(error)
            pass


def setup(bot: commands.Bot):
    bot.add_cog(buy_sell(bot))                    
