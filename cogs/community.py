import disnake
from disnake.ext import commands, tasks
from env import *
from datetime import datetime
import pytz
import numpy as np
from database import Database
import random
from helpers.command_restriction import *



class community(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Community is loaded!")

        # Commands admin
        @commands.default_member_permissions(moderate_members=True)
        @bot.slash_command(description="Verstuur een announcement naar een kanaal!")
        async def announce(inter, channel: disnake.TextChannel, bericht: str):
            try:

                guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
        
                embed=disnake.Embed(title="\n", description=str(bericht), color=0xdf8cfe)
                embed.set_footer(text=f"Deze aankondiging is gemaakt door {inter.author.name}")
                embed.set_thumbnail(url=guild.icon)


                await channel.send(embed=embed)
                mod_log_to_guild(inter, command="announce", user="Geen")
                await inter.response.send_message("Announcement is aangemaakt!", ephemeral=True)
                await log_command(author=inter.author, command="`/announce`", channel=inter.channel)
            except Exception as error:
                await inter.response.send_message(str(error), ephemeral=True)



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
                    if role.permissions.administrator == True or role.permissions.moderate_members == True  or role.permissions.manage_guild == True and value == True:
                        perm_roles.append(perm_name)

            embed.add_field(name=f"Rollen ({len(gebruiker.roles)})", value=str(' '.join(list_roles)), inline=False)
            embed.add_field(name=f"XP", value=str(res[0]), inline=True)
            embed.add_field(name=f"Level", value=str(res[1]), inline=True)
            


        # Commands users
        @commands.cooldown(1, 5.0, commands.BucketType.member)
        @bot.slash_command(description="Kijk of ik nog online ben!")
        async def kapot(inter):
                
                if check_restriction(user_id = inter.author.id, command="/kapot") == False:
                        await inter.response.send_message("Je hebt geen toegang tot dit command. Voor vragen stuur onze bot een DM.",ephemeral=True)
                        return
                else:
                    print(f"User {inter.author.name} gebruikte het command 'kapot'")
                    await inter.response.send_message("Ik ben nog online!")            
                    await log_command(author=inter.author, command="`/kapot`", channel=inter.channel)
                        

        @commands.cooldown(1, 10.0, commands.BucketType.member)
        @bot.slash_command(description="Stuur: Stel gewoon je vraag...")
        async def vraag_om_te_vragen(inter, user: disnake.User):
                
                if check_restriction(user_id = inter.author.id, command="/vraag_om_te_vragen") == False:
                        await inter.response.send_message("Je hebt geen toegang tot dit command. Voor vragen stuur onze bot een DM.",ephemeral=True)
                        return
                else: 
                    print(f"User {inter.author.name} gebruikte het command 'ask'")
                    await inter.send("Verzonden", ephemeral=True)
                    channel = bot.get_channel(inter.channel.id)
                    await channel.send(f"{user.mention}, stel gewoon je vraag, vraag niet om te vragen.")
                    await log_command(author=inter.author, command="`/vraag_om_te_vragen`", channel=inter.channel)
                    return


        @commands.cooldown(1, 10.0, commands.BucketType.member)
        @bot.slash_command(description="Stuur: Dat hoeft niet in DM....")
        async def dm(inter, gebruiker: disnake.User):
                
                if check_restriction(user_id = inter.author.id, command="/dm") == False:
                        await inter.response.send_message("Je hebt geen toegang tot dit command. Voor vragen stuur onze bot een DM.",ephemeral=True)
                        return                
                else:
                    print(f"User {inter.author.name} gebruikte het command 'dm'")
                    await inter.send("Verzonden", ephemeral=True)
                    channel = bot.get_channel(inter.channel.id)        
                    await channel.send(f"{gebruiker.mention}, dat hoeft helemaal niet in een dus doe maar gewoon hier... kunnen andere mensen ook helpen.")
                    await log_command(author=inter.author, command="`/dm`", channel=inter.channel)


        @commands.cooldown(1, 10.0, commands.BucketType.member)
        @bot.slash_command(description="Stuur: Niet zo moeilijk doen...")
        async def moeilijk_doen(inter):
                
                if check_restriction(user_id = inter.author.id, command="/moeilijk_doen") == False:
                        await inter.response.send_message("Je hebt geen toegang tot dit command. Voor vragen stuur onze bot een DM.",ephemeral=True)
                        return
                else:
                    print(f"User {inter.author.name} gebruikte het command 'fok'")
                    await inter.send("Verzonden", ephemeral=True)
                    channel = bot.get_channel(inter.channel.id)        
                    await channel.send("Niet zo moeilijk doen, we helpen je als we kunnen. Totdat we een mooi contract tekenen en je ons gaat betalen, zijn we je niets verplicht.")    
                    await log_command(author=inter.author, command="`/moeilijk_doen`", channel=inter.channel)


        @commands.cooldown(1, 10.0, commands.BucketType.member)
        @bot.slash_command(description="Wijs een lid erop dat het juiste kanaal gebruikt moet worden")
        async def kanaal(inter, user: disnake.User, chnl: disnake.channel.TextChannel):
                
                if check_restriction(user_id = inter.author.id, command="/kanaal") == False:
                        await inter.response.send_message("Je hebt geen toegang tot dit command. Voor vragen stuur onze bot een DM.",ephemeral=True)
                        return
                else:
                    print(f"User {inter.author.name} gebruikte het command 'kanaal'")
                    await inter.send("Verzonden", ephemeral=True)
                    channel = bot.get_channel(inter.channel.id)
                    await channel.send(f"{user.mention}, gelieve het juiste kanaal te gebruik, in dit geval is dat {chnl.mention}.")
                    await log_command(author=inter.author, command="`/kanaal`", channel=inter.channel)


        # ADT&G poll functie
        @bot.slash_command()
        async def poll(inter):
            pass


        @poll.sub_command(description="Maak een nieuwe poll aan!")
        async def toevoegen(inter, poll_vraag, vraag_1, vraag_2, vraag_3 = None, vraag_4 = None
        , vraag_5 = None, vraag_6 = None, vraag_7 = None, vraag_8 = None, vraag_9 = None, vraag_10 = None
        , vraag_11 = None, vraag_12 = None, vraag_13 = None, vraag_14 = None, vraag_15 = None):       

                    if check_restriction(user_id = inter.author.id, command="/verjaardag_toevoegen") == False:
                            await inter.response.send_message("Je hebt geen toegang tot dit command. Voor vragen stuur onze bot een DM.",ephemeral=True)
                            return
                    else:
                        embed = await poll(inter, poll_vraag, vraag_1, vraag_2, vraag_3, vraag_4, vraag_5, vraag_6
                            , vraag_7, vraag_8, vraag_9, vraag_10, vraag_11, vraag_12, vraag_13, vraag_14, vraag_15)

                        msg_sended = await inter.response.send_message(embed=embed)
                        msg = await inter.original_message()

                        await msg.add_reaction("🇦")
                        await msg.add_reaction("🇧")
                        
                        if vraag_3 != None:
                            await msg.add_reaction("🇨")
                        if vraag_4 != None:
                            await msg.add_reaction("🇩")
                        if vraag_5 != None:
                            await msg.add_reaction("🇪")
                        if vraag_6 != None:
                            await msg.add_reaction("🇫")
                        if vraag_7 != None:
                            await msg.add_reaction("🇬")
                        if vraag_8 != None:
                            await msg.add_reaction("🇭")      
                        if vraag_9 != None:
                            await msg.add_reaction("🇮")
                        if vraag_10 != None:
                            await msg.add_reaction("🇯")
                        if vraag_11 != None:
                            await msg.add_reaction("🇰")
                        if vraag_12 != None:
                            await msg.add_reaction("🇱")
                        if vraag_13 != None:
                            await msg.add_reaction("🇲")
                        if vraag_14 != None:
                            await msg.add_reaction("🇴")       
                        if vraag_15 != None:
                            await msg.add_reaction("🇵")                                                                                              
                        
                        await log_command(author=inter.author, command="`/poll toevoegen`", channel=inter.channel)


        @poll.sub_command(description="Krijg alle reacties te zien!")
        async def resultaat(inter, msg_id):

                msg = await inter.channel.fetch_message(msg_id)
                reactions = msg.reactions
                embeds = msg.embeds
                for embed in embeds:
                    embed_content  = embed.to_dict() 
                
                embed = poll_resultaat(reactions, embed_content)
                await inter.response.send_message(embed=embed)
                await log_command(author=inter.author, command="`/poll resultaat`", channel=inter.channel)


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






        # Functions
        # Creating a poll, 15 options
        async def poll(inter, poll_vraag, vraag_1, vraag_2, vraag_3, vraag_4, vraag_5, vraag_6
                        , vraag_7, vraag_8, vraag_9, vraag_10, vraag_11, vraag_12, vraag_13, vraag_14, vraag_15):

            embed=disnake.Embed(title="Poll", description=f"**{poll_vraag}**", color=0xdf8cfe)
            embed.add_field(name=f"🇦 - {vraag_1}", value="\u200b", inline=False)
            embed.add_field(name=f"🇧 - {vraag_2}", value="\u200b", inline=False)
            
            if vraag_3 != None:
                embed.add_field(name=f"🇨 - {vraag_3}", value="\u200b", inline=False)
            if vraag_4 != None:
                embed.add_field(name=f"🇩 - {vraag_4}", value="\u200b", inline=False)
            if vraag_5 != None:
                embed.add_field(name=f"🇪 - {vraag_5}", value="\u200b", inline=False)        
            if vraag_6 != None:
                embed.add_field(name=f"🇫 - {vraag_6}", value="\u200b", inline=False)        
            if vraag_7 != None:
                embed.add_field(name=f"🇬 - {vraag_7}", value="\u200b", inline=False)        
            if vraag_8 != None:
                embed.add_field(name=f"🇭  - {vraag_8}", value="\u200b", inline=False)
            if vraag_9 != None:
                embed.add_field(name=f"🇮 - {vraag_9}", value="\u200b", inline=False)
            if vraag_10 != None:
                embed.add_field(name=f"🇯 - {vraag_10}", value="\u200b", inline=False)         
            if vraag_11 != None:
                embed.add_field(name=f"🇰 - {vraag_11}", value="\u200b", inline=False)        
            if vraag_12 != None:
                embed.add_field(name=f"🇱 - {vraag_12}", value="\u200b", inline=False)        
            if vraag_13 != None:
                embed.add_field(name=f"🇲 - {vraag_13}", value="\u200b", inline=False)        
            if vraag_14 != None:
                embed.add_field(name=f"🇴 - {vraag_14}", value="\u200b", inline=False)        
            if vraag_15 != None:
                embed.add_field(name=f"p - {vraag_15}", value="\u200b", inline=False)   

            guild = await bot.fetch_guild(env_variable.GUILD_ID)
            embed.set_thumbnail(url=guild.icon)

            embed.set_footer(text=f"Deze poll is gemaakt door {inter.author.name}")

            return embed



        # Gets result of a poll by ID
        def poll_resultaat(reactions, embed_content):

                # Storing embed and count info
                data_files = {}

                # Adding embed info to lists
                index_counter = 0
                for emoji in reactions:
                    data_files[index_counter] = {
                        "count": emoji.count,
                        "emoji": emoji.emoji,
                        "question": None
                    }
                    index_counter = index_counter + 1

                index_counter_second = 0
                for name in embed_content["fields"]:
                    question_option = str(name["name"]).split("-")[1]
                    data_files[index_counter_second]["question"] = question_option
                    index_counter_second = index_counter_second + 1
                

                embed=disnake.Embed(title="Uitslag van de poll:", description=embed_content["description"], color=0xdf8cfe)

                # Sorting DATA
                def get_random(item):
                    skills = item[1]["count"]
                    return skills

                sorted_data = sorted(data_files.items(), key=get_random, reverse=True)

                for data in sorted_data:
                    count = int(data[1]["count"]) - 1
                    embed.add_field(name=data[1]["question"], value=f"Stemmen: {count}", inline=False)        

                return embed
        







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