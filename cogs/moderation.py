import disnake
from disnake.ext import commands, tasks
from env import *
from datetime import datetime
import pytz



class moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        tz_AM = pytz.timezone('Europe/Amsterdam') 


        # Commands 
        @commands.default_member_permissions(moderate_members=True)
        @bot.slash_command()
        async def mod(inter):
            pass


        # Warn a member
        @mod.sub_command(description = "Unmute een lid")
        async def warning(inter, gebruiker: disnake.Member, reden: str):

            embed=disnake.Embed(title=f"Waarschuwing voor {gebruiker.name}", description=f"Reden: {reden}", color=disnake.Color.red())
            await inter.response.send_message(embed=embed)

            await event_dm_user(id=gebruiker.id, type="warning", reason=reden)
            # Logging
            usr_name = gebruiker.name
            await mod_log_to_guild(inter, command="mod warning", user=usr_name)


        # Muting member
        @mod.sub_command(description = "Mute een lid")
        async def mute(inter, gebruiker: disnake.Member, reden: str, time: int = commands.Param(name="tijd", choices= {"1 uur": 3600,
            "12 uur": 43200, "1 dag": 86400, "2 dagen": 172800, "3 dagen": 259200})
            ):
            await gebruiker.timeout(duration=time, reason=reden)
            await event_dm_user(id=gebruiker.id, type="time_out_added", reason=reden)
            await inter.response.send_message(f"Met mijn superkrachten heb ik {gebruiker.name} een timeout kunnen geven van {time} seconden!", ephemeral=True)
            # Logging
            usr_name = gebruiker.name
            await mod_log_to_guild(inter=inter, command="mod mute", user=usr_name)


        # Unmutem a member
        @mod.sub_command(description = "Unmute een lid")
        async def unmute(inter, gebruiker: disnake.Member):
            await gebruiker.edit(timeout=False)
            await inter.response.send_message(f"Met mijn superpowwaaah heb ik van {gebruiker.name} de timeout verwijderd!", ephemeral=True)
            await event_dm_user(id= gebruiker.id, type="time_out_removed", reason=None)
            # Logging
            usr_name = gebruiker.name
            await mod_log_to_guild(inter, command="mod unmute", user=usr_name)


        # Member ban
        @mod.sub_command(description = "Ban een lid van de guild!")
        async def ban(inter, gebruiker: disnake.Member, reden: str, verwijder_berichten_dagen: int = commands.Param(name="dagen", choices={"Niks": 0, "1 dag": 1, "2 dagen": 2, 
            "3 dagen": 3, "4 dagen": 4, "5 dagen": 5, "6 dagen": 6, "7 dagen": 7})):
            await event_dm_user(id=gebruiker.id, type="ban_added", reason=reden)
            await gebruiker.ban(reason=reden)
            await inter.response.send_message(f"Met mijn botpowwerrtttt heb ik {gebruiker.name}= gebanned!", ephemeral=True)
            usr_name = gebruiker.name
            await mod_log_to_guild(inter, command="mod ban", user=usr_name)
            await add_user_to_ban_log(inter, usr_name, reden)


        # member unban
        @mod.sub_command(description = "Unban een lid van de guild!")
        async def unban(inter, gebruiker):
            await (await bot.fetch_guild(int(env_variable.GUILD_ID))).unban(gebruiker)
            await inter.response.send_message(f"Met mijn magische krachten heb ik {gebruiker.name}= un-banned!", ephemeral=True)
            #await event_dm_user(id=gebruiker, type="ban_added", reason=None)
            await mod_log_to_guild(inter, command="mod unban", user=gebruiker)


        # Delete multiple messages
        @commands.default_member_permissions(moderate_members=True)
        @bot.slash_command(description="Verwijder meerdere berichten tegelijk!")
        async def verwijder(inter, berichten_aantal: int):

            await inter.channel.purge(limit=berichten_aantal)
            await inter.response.send_message(f"Ik heb {berichten_aantal} berichten verwijderd!", delete_after=4.0)  
            # Logging
            info_logging_to_guild(inter, log="Bulk berichten verwijderd", user=inter.author.name, channel=inter.channel.name, command="`verwijder`")




        # Functions
        async def event_dm_user(id, type, reason=None):
            # Getting user
            user = bot.get_user(id)

            match type:
                
                case "time_out_added":
                    embed=disnake.Embed(title="Je hebt een timeout ontvangen", description=f"Server: AllDayTechAndGaming", color=disnake.Color.red())
                    if reason != None:
                        embed.add_field(name=f"Reden:", value=str(reason), inline=False)
                    embed.add_field(name=f"Wil je de moderatie-actie aanvechten, dan kan je het volgende formulier gebruiken:", value="https://alldaytechandgaming.nl/moderatie-actie-aanvechten-2/", inline=False)
                    embed.set_footer(text=f"Datum: {str(datetime.now(pytz.timezone('Europe/Amsterdam') ))[0:19]}")
                    await user.send(embed=embed)

                case "time_out_removed":
                    embed=disnake.Embed(title="De timeout is eraf gehaald!", description=f"Server: AllDayTechAndGaming", color=disnake.Color.dark_green())
                    embed.set_footer(text=f"Datum: {str(datetime.now(pytz.timezone('Europe/Amsterdam') ))[0:19]}")
                    await user.send(embed=embed)

                case "ban_added":
                    embed=disnake.Embed(title="Je bent gebanned!", description=f"Server: AllDayTechAndGaming", color=disnake.Color.red())
                    if reason != None:
                        embed.add_field(name=f"Reden:", value=str(reason), inline=False)                    
                    embed.add_field(name=f"Wil je de moderatie-actie aanvechten, dan kan je het volgende formulier gebruiken:", value="https://alldaytechandgaming.nl/moderatie-actie-aanvechten-2/", inline=False)
                    embed.set_footer(text=f"Datum: {str(datetime.now(pytz.timezone('Europe/Amsterdam') ))[0:19]}")
                    await user.send(embed=embed)

                case "warning":
                    embed=disnake.Embed(title="Je hebt een waarschuwing gekregen!", description=f"Server: AllDayTechAndGaming", color=disnake.Color.red())
                    embed.add_field(name=f"Reden:", value=str(reason), inline=False)             
                    embed.add_field(name=f"Wil je de moderatie-actie aanvechten, dan kan je het volgende formulier gebruiken:", value="https://alldaytechandgaming.nl/moderatie-actie-aanvechten-2/", inline=False)
                    embed.set_footer(text=f"Datum: {str(datetime.now(pytz.timezone('Europe/Amsterdam') ))[0:19]}")
                    await user.send(embed=embed)



        # Sending stuff to LOG channel
        def mod_log_to_guild(inter, command, user):
            channel_to_send = bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)

            embed=disnake.Embed(title="Adje log", description=f"Op gebruiker: {user}", color=disnake.Color.dark_green())
            embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
            embed.add_field(name=f"Command gebruikt:", value=str(command), inline=True)
            embed.add_field(name=f"Kanaal:", value=str(inter.channel.name), inline=True)
            embed.set_footer(text=f"Datum: {str(datetime.now(pytz.timezone('Europe/Amsterdam') ))[0:19]}")

            bot.loop.create_task(channel_to_send.send(embed=embed))



        async def add_user_to_ban_log(inter, usr_name, reden):
            embed=disnake.Embed(title=f"User '{usr_name}' gebanned", description=f"Door: {inter.author.mention}", color=disnake.Color.purple())
            embed.add_field(name="Reden:", value=str(reden), inline=False)
            channel_to_send = bot.get_channel(env_variable.BAN_LOG)
            await channel_to_send.send(embed=embed)
        


        # Sending stuff to LOG channel
        def info_logging_to_guild(log, user, channel, command=None, inter=None):
            channel_to_send = bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)

            embed=disnake.Embed(title="Adje log", description="Info", color=0xdf8cfe)

            if inter != None:
                embed.set_author(name=user, icon_url=inter.author.avatar)
            embed.add_field(name=f"Log gebeurtenis:", value=str(log), inline=True)
            if command != None:
                embed.add_field(name=f"Command:", value=str(command), inline=True)

            embed.add_field(name=f"Kanaal:", value=str(channel), inline=True)
            embed.set_footer(text=f"Datum: {str(datetime.now(tz_AM))[0:19]}")

            bot.loop.create_task(channel_to_send.send(embed=embed))



def setup(bot: commands.Bot):
    bot.add_cog(moderation(bot))