import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import MissingPermissions
from disnake.enums import ButtonStyle
import datetime
from datetime import timedelta
import mysql.connector
import random
from datetime import datetime
import threading 
from threading import Timer
from env import *
from datetime import datetime
import pytz
import random
import asyncio
from database import *
import urllib.request
from helpers.command_restriction import *



class Leveling(commands.Cog):
    


    def __init__(self, bot: commands.Bot):

        self.intents = disnake.Intents.all()
        self.bot = bot

        # Time stuffies
        self.tz_AM = pytz.timezone('Europe/Amsterdam') 
        self.datetime_AM = datetime.now(self.tz_AM) 
        self.time_now = self.datetime_AM.strftime("%H:%M:%S")

        self.users =[]
        self.messaged = []
        self.guild = []

        self.vChannels = [env_variable.V_CHANNEL_ONE, env_variable.V_CHANNEL_TWO]
        self.levelRoles = [768381227497029632, 768381279582027796, 768381333259943946, 768381397412478977, 768381462314483712, 768382361342836766, 768382540917506058, 768382615027449876, 768382797214777374, 768382928790749184, 959422205240946718, 959422412204691506, 959739023822323782, 959739123437031455, 959740858461224960, 959741104733966436, 959741224594604032, 959741349211553842, 959741768356728955, 959741830570848296]



    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing , name="DM om beheer te contacteren"))
            global guild    
            global channel
            guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
            print("The bot is ready!")

        except Exception as error:
            print(error)
            pass

        
        Leveling.debug(type="Adje restart", data="No data", error="No error")
        Leveling.basic_log(self, log="Reboot")
        


        self.minute.start()



    # On message
    @commands.Cog.listener()
    async def on_message(self, m):
        global messaged

        # Checks if msg is in tech-news
        if m.channel.id == env_variable.TECH_NEWS_ID:
            
            channel = self.bot.get_channel(env_variable.TECH_NEWS_ID)
            message = await channel.fetch_message(channel.last_message_id)
            await message.publish()
            return


        # check if message is send from a bot, then do nothing
        if m.author == self.bot.user or m.author.bot:
            return
        
        elif isinstance(m.channel, disnake.channel.DMChannel):
            return

        # 
        if m.content.lower().startswith("ad."):
            pass
        else:
            id = m.author.id
            if id in messaged:
                return
            else:
                messaged.append(id)
                Leveling.gainXP(self, id, xp_amount=Leveling.get_xp_amount_value(msg_or_vc="message"))



    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print("Cleaning User and birthday_users tables!")
        # If member leaves, clear DB
        await Leveling.member_leave_dbClean()
        # If member leaves, remove from birthday
        await Leveling.member_leave_birthday_clear(user_id=member.id)


    # Slash commands
    @commands.slash_command(description="Zie de level van de members van ADT&G!")
    async def scorebord(self, inter, pagina: int = 1):
                print(f"User {inter.author.display_name} gebruikte het command 'leaderboard'")
                p = 0
                p = pagina
                p = p - 1
                
                e = await Leveling.levelLeaderboard(self, p)
                if e is None:
                    await inter.response.send_message("Er ging iets mis. Oepsie!")
                else:
                    await inter.response.send_message(embed=e)


    @commands.slash_command(description="Zie je eigen level!")
    async def level(self, inter):
                print(f"User {inter.author.display_name} gebruikte het command 'level'")
                id = inter.author.id
                e = await Leveling.levelMessage(self, id)
                if e is None:
                    await inter.response.send_message("Er ging iets mis. Oepsie!")
                else:
                    await inter.response.send_message(embed=e)


    @commands.slash_command(description="Bereken je level!")
    async def level_calc(self, inter, level: int):
                print(f"User {inter.author.display_name} gebruikte het command 'level_calc'")
                lvl = level
                e = await Leveling.levelCalc(self, inter.author.id, lvl)
                if e is None:
                    await inter.response.send_message("Er ging iets mis. Oepsie!")
                else:
                    await inter.response.send_message(embed=e)


    @commands.slash_command(description="Bedank iemand!")
    async def bedank(self, inter, gebruiker: disnake.User, reden: str = "Geen reden opgegeven"):
                
                if gebruiker == self.bot or gebruiker == self.bot.user:
                    await inter.response.send_message(f"{inter.author.display_name}, je mag de bot niet bedanken. Gebruik deze functie niet voor onnodige bedankjes!")
                    return

                if check_restriction(user_id = inter.author.id, command="/bedank") == False:
                        await inter.response.send_message("Je hebt geen toegang tot dit commando. Voor vragen stuur onze bot een direct bericht.",ephemeral=True)
                        return
                else: 
                    print(f"User {inter.author.display_name} gebruikte het command 'thank'")
                    e = await Leveling.thank(self, inter, gebruiker, reden)
                    if e is None:
                        await inter.response.send_message("Er ging iets mis. Oepsie!")
                    else:
                        await inter.response.send_message(embed=e)


    @commands.slash_command(description="Comp-leaderboard")
    async def comp_scorebord(self, inter, pagina: int):
                print(f"User {inter.author.display_name} gebruikte het command 'compleaderboard'")

                p = pagina
                p = p - 1
                e = await Leveling.compLeaderboard(self, p)
                if e is None:
                    await inter.response.send_message("Er ging iets mis. Oepsie!")
                else:
                    await inter.response.send_message(embed=e)



    # Functions
    async def member_leave_dbClean():
        global users
        global guild
        presentids = []
        members = await guild.fetch_members(limit=1000).flatten()
        for member in members:
            presentids.append(member.id)

        Database.cursor.execute("SELECT * FROM Users")
        sqlids = Database.cursor.fetchall()
        i = 0
        while i < len(sqlids):
            if sqlids[i][0] in presentids:
                print(str(sqlids[i][0]) + " is still here")
            else:
                print("removing user with ID: " + str(sqlids[i][0]))
                Leveling.delete_user(sqlids[i][0])

            i = i + 1  



    async def member_leave_birthday_clear(user_id):
        try:
            Database.cursor.execute(f"DELETE FROM birthday_users WHERE user_id={user_id}")
            Database.db.commit()
        except Exception as error:
            pass



    def gainXP(self, id, xp_amount):
        print("Gaining XP for user: " + str(id))
        x = xp_amount

        val_user = Leveling.validate_user_in_db(self, id) 
        
        if val_user == False:
            Leveling.create_user(id, x)
            Leveling.debug(type="Creating user", data=str(id), error="None")

        else:
            xp = Leveling.get_xp(self, id)
            level = Leveling.get_level(id)

            xp = xp + x
            levelxpcap = int(8.196 * pow(level + 1, 2.65) + 200)

            if xp > levelxpcap:
                level = level + 1
                self.bot.loop.create_task(Leveling.gainLevel(self, id, level))
                Leveling.set_level(id, level)

            else:
                Leveling.set_xp(self, id, xp)
    


    async def gainLevel(self, id, level):
        print("Leveling user " + str(id) + " to level " + str(level))
        channel = self.bot.get_channel(Channel.ALLDAYBOT)
        guild = await self.bot.fetch_guild(env_variable.GUILD_ID)

        name = (await self.bot.get_or_fetch_user(id)).display_name 
        name_avatar = (await self.bot.get_or_fetch_user(id)).avatar
        
        member = await guild.fetch_member(id)

        embed=disnake.Embed(title=f"⚡ Iemand is een level omhoog gegaan!", description=f"{member.mention} gefeliciteerd!", color=0xdf8cfe)
        
        if level%5 == 0:
            rolenum = (level // 5) - 1
            rolenum_rm = (level // 5) - 2

            role = guild.get_role(self.levelRoles[rolenum])
            role_to_rm = guild.get_role(self.levelRoles[rolenum_rm])

            await member.add_roles(role)
            await member.remove_roles(role_to_rm)
            
        if level == 69:
            role = guild.get_role(768382432155533322)
            await member.add_roles(role)
            embed = disnake.Embed(title="Gefeliciteerd!", color=0xdf8cfe, description="Je bent een fucking koning, je hebt level 69 gehaald! Mokergeil pik!")

        if level == 70:
            role = guild.get_role(768382432155533322)
            await member.remove_roles(role)

        embed.add_field(name=f"\n", value=f"📈 Nieuw level: {level}", inline=False)
        embed.add_field(name=f"\n", value=f"📈 Nieuw XP: {Leveling.get_xp(self, id)}", inline=False)
        embed.set_author(name=name, icon_url=name_avatar)
        embed.set_thumbnail(url=guild.icon)
        await channel.send(embed=embed)



    async def levelCalc(self, id, level):

        totalNeeded = int(8.196 * pow((level), 2.65) + 200)
        xp = Leveling.get_xp(self, id)
        userNeeded = int(totalNeeded) - xp     
        guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
        name = (await self.bot.get_or_fetch_user(id)).display_name 
        name_avatar = (await self.bot.get_or_fetch_user(id)).avatar

        embed = disnake.Embed(title=f"⚡ Level berekening voor {name}",description=f"Voor level: **{level}**", color=0xdf8cfe)
        embed.set_author(name=name, icon_url=name_avatar)
        embed.add_field(name="\n", value=f"📈 XP nodig vanaf 0: {totalNeeded}", inline=False)
        embed.add_field(name="\n", value=f"📈 Je huidige XP: {xp}", inline=False)
        embed.add_field(name="\n", value=f"📈 Je hebt dit nog nodig: {userNeeded}", inline=False)
        embed.set_thumbnail(url=guild.icon)

        return embed


        
    async def levelLeaderboard(self, p):
        global guild
        
        try:
            Database.cursor.execute("SELECT id, lvl, xp FROM Users ORDER BY xp DESC")
            users = Database.cursor.fetchall()
        except Exception as e:
            Leveling.debug(type="lvlboard database", data=str(id), error=str(e))
            Leveling.error_logging_to_guild(self, error=e)
        embed = disnake.Embed(title='ADT&G XP scorebord, pagina ' + str(p + 1), color=0xdf8cfe)
            
        i = 0;
        i = i + 10 * p
        p = (p+1) * 10
        postition_count = i  
        
        while i < p and i < len(users):
            text = "Level: " + str(users[i][1]) + ", totale xp: " + str(users[i][2])
            postition_count = postition_count + 1
            user_id = users[i][0]
            name = (await self.bot.get_or_fetch_user(user_id)).display_name             
            embed.add_field(name=f"#{postition_count} - {name}", value=text, inline=False)
            i = i + 1
        
        return embed



    async def compLeaderboard(self, p):

        try:
            Database.cursor.execute("SELECT id, complements FROM Users ORDER BY complements DESC")
            result = Database.cursor.fetchall()
        except Exception as e:
            Leveling.debug(type="compleaderboard database", data=str(id), error=str(e))
            Leveling.error_logging_to_guild(self, error=e)

        embed = disnake.Embed(title='ADT&G complimenten scorebord, pagina ' + str(p + 1), color=0xdf8cfe)
        i = 0;
        i = i + 10 * p
        p = (p+1) * 10
        if i >= len(users):
            embed = disnake.Embed(title="Zoveel pagina's hebben we niet.", color=0xdf8cfe)
            return embed

        while i < p and i < len(users):

            text = "complimenten: " + str(users[i][1])
            user_id = users[i][0]
            name = (await self.bot.get_or_fetch_user(user_id)).display_name 
            
            embed.add_field(name=name, value=text, inline=False)

            i = i + 1
        
        return embed



    async def levelMessage(self, id):
        xp = Leveling.get_xp(self, id)
        level = Leveling.get_level(id)
        complements = Leveling.get_complements(id)

        user = (await self.bot.get_or_fetch_user(id)).display_name
        user_avatar = (await self.bot.get_or_fetch_user(id)).avatar
        guild = await self.bot.fetch_guild(env_variable.GUILD_ID)

        if xp == 0 and level == 0:
            embed = disnake.Embed(title="Er ging iets fout.", color=0xdf8cfe)
            embed.set_author(name=user, icon_url=user_avatar)
            return embed

        needed = int(8.196 * pow((level + 1), 2.65) + 200)
        needed = needed - xp

        embed=disnake.Embed(title=f"⚡ Het profiel van {user}:", description=f"\n", color=0xdf8cfe)
        embed.set_author(name=user, icon_url=user_avatar)
        
        embed.add_field(name=f"\n", value=f"⚡ Huidig level: {level}", inline=False)
        embed.add_field(name=f"\n", value=f"📈 XP nodig: {needed}", inline=False)
        embed.add_field(name=f"\n", value=f"📈 Totale XP: {xp}", inline=False)
        embed.add_field(name=f"\n", value=f"👍 Complimenten: {complements}", inline=False)
        embed.set_thumbnail(url=guild.icon)

        return embed



    def author_check(author):
        return lambda message: message.author == author



    async def thank(self, inter, gebruiker, reden):
        global users
        if inter.author.id == gebruiker.id:
            
            e = disnake.Embed(title="Je kan jezelf niet bedanken, pannekoek!", color=0xdf8cfe)
            e.set_author(name=inter.author.display_name, icon_url=inter.author.avatar)
            e.add_field(name="Wat denk je nou joh", value="Mafklapper!")
            return e
        
        get_actual_daily_compliments = Leveling.get_dailycomplements(inter.author.id)
        if get_actual_daily_compliments > 2:
            e = disnake.Embed(title="Je hebt niet genoeg complimenten over vandaag!", color=0xdf8cfe)
            e.set_author(name=inter.author.display_name) #, icon_url=m.author.avatar_url
            e.add_field(name="Complimenten over vandaag: ", value=get_actual_daily_compliments - 3, inline=True)
            e.add_field(name="Gecomplimenteerde users: ", value=get_actual_daily_compliments, inline=True)
            
        else:
            user = (await self.bot.get_or_fetch_user(gebruiker.id)).name
            
            Leveling.set_dailycomplements(inter.author.id, get_actual_daily_compliments + 1)
            e = disnake.Embed(title="Complimenten", color=disnake.Color.green())
            e.set_author(name=inter.author.display_name, icon_url=inter.author.avatar)

            complements = Leveling.get_complements(gebruiker.id)
            Leveling.set_complements(gebruiker.id, complements + 1)
            Leveling.gainXP(self, gebruiker.id, xp_amount=150)
            e.add_field(name="Compliment gegeven aan", value=user)
            e.add_field(name="Reden", value=reden)


        return e



    def set_xp(self, id, xp):

        try:
            Database.cursor.execute("UPDATE Users SET xp = " + str(xp) + " WHERE id = " + str(id))
            Database.db.commit()
        except Exception as e:
            Leveling.debug(type="set_xp database", data=str(id), error=str(e))
            Leveling.error_logging_to_guild(self, error=e)



    def get_xp(self, id):

            try:
                Database.cursor.execute("SELECT xp FROM Users WHERE id = " + str(id))
                result = Database.cursor.fetchone()[0]
                return result
            except Exception as e:
                Leveling.debug(type="get_xp database", data=str(id), error=str(e))
                Leveling.error_logging_to_guild(self, error=e)



    def set_level(id, lvl):

        try:
            Database.cursor.execute("UPDATE Users SET lvl = " + str(lvl) + " WHERE id = " + str(id))
            Database.db.commit()
        except Exception as e:
            Leveling.debug(type="set_level database", data=str(id), error=str(e))
            Leveling.error_logging_to_guild(error=e)    



    def get_level(id):
        Database.cursor.execute("SELECT lvl FROM Users WHERE id=" + str(id))
        if Database.cursor.rowcount == 0:
            return 0
        else:

            try:
                result = Database.cursor.fetchone()[0]
                return result

            except Exception as e:
                Leveling.debug(type="get_level database", data=str(id, result), error=str(e))
                Leveling.error_logging_to_guild(error=e)
                pass
        


    def set_complements(id, complements):
        try:
            Database.cursor.execute("UPDATE Users SET complements = " + str(complements) + " WHERE id = " + str(id))
            Database.db.commit()
        except Exception as e:
            Leveling.debug(type="set_complements database", data=str(id), error=str(e))
            Leveling.error_logging_to_guild(error=e)



    def get_complements(id):
        Database.cursor.execute("SELECT complements FROM Users WHERE id = " + str(id))
        if Database.cursor.rowcount == 0:
            return 0
        else:

            try:
                result = Database.cursor.fetchone()[0]
            except Exception as e:
                Leveling.debug(type="get_complements database", data=str(id), error=str(e))
                Leveling.error_logging_to_guild(error=e)
            return result



    def set_dailycomplements(id, dailycomplements):

        try:
            Database.cursor.execute("UPDATE Users SET dailycomplements = " + str(dailycomplements) + " WHERE id = " + str(id))
            Database.db.commit()
        except Exception as e:
            Leveling.error_logging_to_guild(error=e)
            Leveling.debug(type="set_dailycomplements database", data=str(id), error=str(e))



    def get_dailycomplements(id):

        Database.cursor.execute("SELECT dailycomplements FROM Users WHERE id = " + str(id))
        if Database.cursor.rowcount == 0:
            return 0
        else:
            try:
                result = Database.cursor.fetchone()[0]
            except Exception as e:
                Leveling.debug(type="get_dailycomplements database", data=str(id), error=str(e))
                Leveling.error_logging_to_guild(error=e)
            return result


    @tasks.loop(seconds=30) 
    async def reset_daily_comps():
            datetime_AM = datetime.now(pytz.timezone('Europe/Amsterdam') )
            now_time = datetime_AM.strftime("%H%M")

            if now_time == "0300":
                Database.cursor.execute("UPDATE Users SET dailycomplements=0")
                Database.db.commit()
                print("Daily comp reset")

    reset_daily_comps.start()



    def create_user(id, xp):

        try:
            Database.cursor.execute("INSERT INTO Users(id, xp, lvl, dailycomplements, complements) VALUES ("+ str(id) + ", " + str(xp) + ", 0, 0, 0);")
            Database.db.commit()
        except Exception as e:
            Leveling.debug(type="create_user database", data=str(id), error=str(e))
            Leveling.error_logging_to_guild(error=e)


    def delete_user(id):

        try:
            Database.cursor.execute("DELETE FROM Users WHERE id = " + str(id))
            Database.db.commit()
        except Exception as e:
            Leveling.debug(type="delete_user database", data=str(id), error=str(e))        
            Leveling.error_logging_to_guild(error=e)



    
    @tasks.loop(seconds=60.0)
    async def minute(self):

        try:
            global messaged
            global vChannels
            global users
            messaged = []

            print("A minute has passed!")
            for vChannel in self.vChannels:
                channel = self.bot.get_channel(vChannel)
                if len(channel.members) > 1:
                    for member in channel.members:
                        if not(member.voice.afk or member.voice.mute or member.voice.deaf or member.voice.self_mute or member.voice.self_deaf):
                            Leveling.gainXP(self, member.id, xp_amount=Leveling.get_xp_amount_value(msg_or_vc="voicechat"))


        except Exception as error:
            print(error)



    # DEBUGGING
    def debug(type, data, error):
        print(f"**Type:** {type} -- **Data:** {data} -- **Python exception:** {error}")



    # validate users
    def validate_user_in_db(self, id):
        try: 
            # Get user
            Database.cursor.execute(f"select xp from Users WHERE id={id}")
            query = Database.cursor.fetchone()

            if query == None:
                return False
            elif query == {}:
                return False
            else:
                return True

        except Exception as e:
            # DEBUGGING
            print(f"DEBUGGING: Error: {e}")
            Leveling.error_logging_to_guild(self, error=e)
            pass
        


    def get_xp_amount_value(msg_or_vc):
        if msg_or_vc == "message":
            Database.cursor.execute("SELECT xp_messages FROM bot_settings LIMIT 1")
        else:
            Database.cursor.execute("SELECT xp_voicechat FROM bot_settings LIMIT 1")

        res = Database.cursor.fetchone()[0]
        return res



    # Basic log function
    def basic_log(self, log):
        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)

        embed=disnake.Embed(title="Adje log", description=str(log), color=disnake.Color.green())
        embed.set_footer(text=f"Datum: {str(datetime.now(self.tz_AM))[0:19]}")

        self.bot.loop.create_task(channel_to_send.send(embed=embed))



    # Sending stuff to LOG channel
    def error_logging_to_guild(self, error):
        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)

        embed=disnake.Embed(title="Adje log", description="Error", color=0xdf8cfe)
        embed.add_field(name=f"Error data:", value=str(error), inline=True)
        embed.set_footer(text=f"Datum: {str(datetime.now(self.tz_AM))[0:19]}")

        self.bot.loop.create_task(channel_to_send.send(embed=embed))


def setup(bot: commands.Bot):
    bot.add_cog(Leveling(bot))