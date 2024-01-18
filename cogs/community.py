import disnake
from disnake.ext import commands, tasks
from env import *
from datetime import datetime
import pytz
import numpy as np
from database import Database
import random



class community(commands.Cog):


    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Community is loaded!")



        @commands.default_member_permissions(moderate_members=True)
        @bot.slash_command(description="Zie alle info over een gebruiker")
        async def gebruiker_info(inter, gebruiker: disnake.Member):

            embed=disnake.Embed(title="Gebruiker informatie", description=gebruiker.mention, color=0xdf8cfe)
            embed.set_author(name=gebruiker.name, icon_url=gebruiker.avatar)
            embed.add_field(name=f"Gejoined", value=str(gebruiker.joined_at).split(".")[0], inline=True)
            embed.add_field(name=f"Geregistreerd", value=str(gebruiker.created_at).split(".")[0], inline=True)
            embed.set_thumbnail(url=gebruiker.avatar)

            list_roles = []
            perm_roles = []

            # Getting xp and level from user
            Database.cursor.execute(f"SELECT XP, LVL FROM Users WHERE id={gebruiker.id} LIMIT 1")
            res = Database.cursor.fetchone()

            for role in gebruiker.roles:
                list_roles.append(role.mention)

                for perm_name, value in role.permissions:
                    #if role.permissions.administrator == True or role.permissions.moderate_members == True or role.permissions.manage_guild == True and value == True:
                    if value == True:
                        perm_roles.append(perm_name)

            embed.add_field(name=f"Rollen ({len(gebruiker.roles)})", value=str(' '.join(list_roles)), inline=False)
            embed.add_field(name=f"XP", value=str(res[0]), inline=True)
            embed.add_field(name=f"Level", value=str(res[1]), inline=True)
            await inter.response.send_message(embed=embed, ephemeral=True)

            print(perm_roles)


        # Commands users
        @commands.cooldown(1, 5.0, commands.BucketType.member)
        @bot.slash_command(description="Kijk of ik nog online ben!")
        async def kapot(inter):

            print(f"User {inter.author.name} gebruikte het command 'kapot'")
            await inter.response.send_message("Ik ben nog online!")            
            await log_command(author=inter.author, command="`/kapot`", channel=inter.channel)
                

        @commands.cooldown(1, 10.0, commands.BucketType.member)
        @bot.slash_command(description="Stuur: Stel gewoon je vraag...")
        async def vraag_om_te_vragen(inter, user: disnake.User):
                
            print(f"User {inter.author.name} gebruikte het command 'ask'")
            await inter.send("Verzonden", ephemeral=True)
            channel = bot.get_channel(inter.channel.id)
            await channel.send(f"{user.mention}, stel gewoon je vraag, vraag niet om te vragen.")
            await log_command(author=inter.author, command="`/vraag_om_te_vragen`", channel=inter.channel)
            return


        @commands.cooldown(1, 10.0, commands.BucketType.member)
        @bot.slash_command(description="Stuur: Dat hoeft niet in DM....")
        async def dm(inter, gebruiker: disnake.User):
                
            print(f"User {inter.author.name} gebruikte het command 'dm'")
            await inter.send("Verzonden", ephemeral=True)
            channel = bot.get_channel(inter.channel.id)        
            await channel.send(f"{gebruiker.mention}, dat hoeft helemaal niet in een DM dus doe maar gewoon hier... kunnen andere mensen ook helpen.")
            await log_command(author=inter.author, command="`/dm`", channel=inter.channel)


        @commands.cooldown(1, 10.0, commands.BucketType.member)
        @bot.slash_command(description="Stuur: Niet zo moeilijk doen...")
        async def moeilijk_doen(inter):
                
            print(f"User {inter.author.name} gebruikte het command 'fok'")
            await inter.send("Verzonden", ephemeral=True)
            channel = bot.get_channel(inter.channel.id)        
            await channel.send("Niet zo moeilijk doen, we helpen je als we kunnen. Totdat we een mooi contract tekenen en je ons gaat betalen, zijn we je niets verplicht.")    
            await log_command(author=inter.author, command="`/moeilijk_doen`", channel=inter.channel)


        @commands.cooldown(1, 10.0, commands.BucketType.member)
        @bot.slash_command(description="Wijs een lid erop dat het juiste kanaal gebruikt moet worden")
        async def kanaal(inter, user: disnake.User, chnl: disnake.channel.TextChannel):
                
            print(f"User {inter.author.name} gebruikte het command 'kanaal'")
            await inter.send("Verzonden", ephemeral=True)
            channel = bot.get_channel(inter.channel.id)
            await channel.send(f"{user.mention}, gelieve het juiste kanaal te gebruik, in dit geval is dat {chnl.mention}.")
            await log_command(author=inter.author, command="`/kanaal`", channel=inter.channel)


        @commands.cooldown(1, 2.0, commands.BucketType.member)
        @bot.slash_command(description="Krijg een random antwoord terug!")
        async def random_woord(inter, input_1, input_2, input_3 = None, input_4 = None, input_5 = None):
                list_inputs = []
                list_inputs.append(input_1)
                list_inputs.append(input_2)
                if input_3 != None:
                    list_inputs.append(input_3)
                if input_4 != None:
                    list_inputs.append(input_4)
                if input_5 != None:
                    list_inputs.append(input_5)            

                embed=disnake.Embed(title="Random antwoord:", description=f"**{random.choice(list_inputs)}**", color=0xdf8cfe)
                await inter.response.send_message(embed=embed)
                await log_command(author=inter.author, command="`/random_woord`", channel=inter.channel)


        @commands.cooldown(1, 2.0, commands.BucketType.member)
        @bot.slash_command(description="Krijg een getal uit je opgegeven range terug!")
        async def random_range(inter, range_nummer: int):
                list_inputs = []
                for i in range(range_nummer):
                    list_inputs.append(i + 1)
                    
                embed=disnake.Embed(title="Random nummer uit je range:", description=f"{random.choice(list_inputs)}", color=0xdf8cfe)
                await inter.response.send_message(embed=embed)
                list_inputs.clear

                await log_command(author=inter.author, command="`/random_range`", channel=inter.channel)


        # Cooldown message
        @moeilijk_doen.error
        @dm.error
        @vraag_om_te_vragen.error
        @kapot.error
        @random_woord.error
        @random_range.error
        async def test_error(inter: disnake.GuildCommandInteraction, error: Exception) -> None:
            if isinstance(error, commands.CommandOnCooldown):
                new_error = str(error).split(" ")[7]
                return await inter.response.send_message(
                    f"Deze command heeft een cooldown, probeer het over `{new_error}` opnieuw.", ephemeral=True
                )



        # Functions
        # Sending stuff to LOG channel
        def mod_log_to_guild(inter, command, user):
            channel_to_send = bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)

            embed=disnake.Embed(title="Adje log", description=f"Op gebruiker: {user}", color=disnake.Color.dark_green())
            embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
            embed.add_field(name=f"Command gebruikt:", value=str(command), inline=True)
            embed.add_field(name=f"Kanaal:", value=str(inter.channel.name), inline=True)
            embed.set_footer(text=f"Datum: {str(datetime.now(pytz.timezone('Europe/Amsterdam') ))[0:19]}")

            bot.loop.create_task(channel_to_send.send(embed=embed))



        # Command logging
        async def log_command(author, command, channel):

            embed=disnake.Embed(title=f"Een user heeft een command gebruikt!", description=f"\n", color=disnake.Color.green())
            embed.add_field(name="Command::", value=str(command), inline=True)
            embed.add_field(name="Author:", value=str(author.mention), inline=True)
            embed.add_field(name="Kanaal:", value=str(channel.mention), inline=False)
            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await channel_to_send.send(embed=embed)




def setup(bot: commands.Bot):
    bot.add_cog(community(bot))