# TODO Fix ModMail in Adje
# TODO fix nixs
import disnake
from disnake.ext import commands, tasks
from disnake.ext.commands import MissingPermissions
from disnake.enums import ButtonStyle
import datetime
from datetime import timedelta
import mysql.connector
import random
import time, schedule
from datetime import datetime
import threading 
from threading import Timer
from env import *
from datetime import datetime
import pytz
import random
import asyncio
from database import *


# Time stuffies
tz_AM = pytz.timezone('Europe/Amsterdam') 
datetime_AM = datetime.now(tz_AM)
time_now = datetime_AM.strftime("%H:%M:%S")

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)

users =[]
messaged = []
guild = []

vChannels = [env_variable.V_CHANNEL_ONE, env_variable.V_CHANNEL_TWO]
levelRoles = [768381227497029632, 768381279582027796, 768381333259943946, 768381397412478977, 768381462314483712, 768382361342836766, 768382540917506058, 768382615027449876, 768382797214777374, 768382928790749184, 959422205240946718, 959422412204691506, 959739023822323782, 959739123437031455, 959740858461224960, 959741104733966436, 959741224594604032, 959741349211553842, 959741768356728955, 959741830570848296]


@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing , name="DM om beheer te contacteren"))
    global guild    
    global channel
    guild = await bot.fetch_guild(env_variable.GUILD_ID)
    print("The bot is ready!")
    debug(type="Adje restart", data="No data", error="No error")
    basic_log(log="Reboot")
    Minute()
    

            
# On message
@bot.event
async def on_message(m):
    global messaged

    # Checks if msg is in tech-news
    if m.channel.id == env_variable.TECH_NEWS_ID:
        
        channel = bot.get_channel(env_variable.TECH_NEWS_ID)
        message = await channel.fetch_message(channel.last_message_id)
        await message.publish()
        return


    # check if message is send from a bot, then do nothing
    if m.author == bot.user or m.author.bot:
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
            gainXP(id, 15, 25)


# Slash commands
@bot.slash_command(description="Zie de level van de members van ADT&G!")
async def scorebord(inter, pagina: int = 1):
            print(f"User {inter.author.name} gebruikte het command 'leaderboard'")
            p = 0
            p = pagina
            p = p - 1
            
            e = await levelLeaderboard(p)
            if e is None:
                await inter.response.send_message("Er ging iets mis. Oepsie!")
            else:
                await inter.response.send_message(embed=e)


@bot.slash_command(description="Zie je eigen level!")
async def level(inter):
            print(f"User {inter.author.name} gebruikte het command 'level'")
            id = inter.author.id
            e = await levelMessage(id)
            if e is None:
                await inter.response.send_message("Er ging iets mis. Oepsie!")
            else:
                await inter.response.send_message(embed=e)


@bot.slash_command(description="Bereken je level!")
async def level_calc(inter, level: int):
            print(f"User {inter.author.name} gebruikte het command 'level_calc'")
            lvl = level
            e = await levelCalc(inter.author.id, lvl)
            if e is None:
                await inter.response.send_message("Er ging iets mis. Oepsie!")
            else:
                await inter.response.send_message(embed=e)


@bot.slash_command(description="Bedank iemand!")
async def bedank(inter, gebruiker: disnake.User, reden: str = "Geen reden opgegeven"):
            print(f"User {inter.author.name} gebruikte het command 'thank'")
            e = await thank(inter, gebruiker, reden)
            if e is None:
                await inter.response.send_message("Er ging iets mis. Oepsie!")
            else:
                await inter.response.send_message(embed=e)


@bot.slash_command(description="Comp-leaderboard")
async def comp_scorebord(inter, pagina: int):
            print(f"User {inter.author.name} gebruikte het command 'compleaderboard'")

            p = pagina
            p = p - 1
            e = await compLeaderboard(p)
            if e is None:
                await inter.response.send_message("Er ging iets mis. Oepsie!")
            else:
                await inter.response.send_message(embed=e)



@commands.default_member_permissions(moderate_members=True)
@bot.slash_command(description="clear de db.")
async def db_clean(inter):
        print(f"User {inter.author.name} gebruikte het command 'db_clean'")
        await member_leave_dbClean()








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
            delete_user(sqlids[i][0])

        i = i + 1  



def gainXP(id, minxp, maxxp):
    print("gaining XP for user: " + str(id))
    x = random.randint(minxp, maxxp)

    val_user = validate_user_in_db(id) 
    
    if val_user == False:
        create_user(id, x)
        debug(type="Creating user", data=str(id), error="None")

    else:
        xp = get_xp(id)
        level = get_level(id)

        xp = xp + x
        levelxpcap = int(8.196 * pow(level + 1, 2.65) + 200)

        if xp > levelxpcap:
            level = level + 1
            bot.loop.create_task(gainLevel(id, level))
            set_level(id, level)

        else:
            set_xp(id, xp)
  


async def gainLevel(id, level):
    global levelRoles

    print("Leveling user " + str(id) + " to level " + str(level))
    channel = bot.get_channel(768390290225889280)
    
    name = (await bot.get_or_fetch_user(id)).name 
    name_avatar = (await bot.get_or_fetch_user(id)).avatar
    
    member = await guild.fetch_member(id)
    embed = disnake.Embed(title="Gefeliciteerd!", color=0xdf8cfe, description="Je hebt net level " + str(level) + " behaald!")
    if level%5 == 0:
        rolenum = (level // 5) - 1
        rolenum_rm = (level // 5) - 2

        role = guild.get_role(levelRoles[rolenum])
        role_to_rm = guild.get_role(levelRoles[rolenum_rm])

        await member.add_roles(role)
        await member.remove_roles(role_to_rm)
    if level == 69:
        role = guild.get_role(768382432155533322)
        await member.add_roles(role)
        embed = disnake.Embed(title="Gefeliciteerd!", color=0xdf8cfe, description="Je bent een fucking koning, je hebt level 69 gehaald! Mokergeil pik!")
    if level == 70:
        role = guild.get_role(768382432155533322)
        await member.remove_roles(role)
    embed.set_author(name=name, icon_url=name_avatar)
    await channel.send(embed=embed)



async def levelCalc(id, level):
    totalNeeded = int(8.196 * pow((level), 2.65) + 200)
    xp = get_xp(id)

    userNeeded = int(totalNeeded) - xp     

    name = (await bot.get_or_fetch_user(id)).name 
    
    name_avatar = (await bot.get_or_fetch_user(id)).avatar

    embed = disnake.Embed(title='Level berekening voor level: ' + str(level), color=0xdf8cfe)
    embed.set_author(name=name, icon_url=name_avatar)
    embed.add_field(name="XP nodig vanaf 0: ", value = str(totalNeeded), inline=True)
    embed.add_field(name="Je huidige XP: ", value = str(xp), inline=True)
    embed.add_field(name="Je hebt dit nog nodig: ", value = str(userNeeded), inline=True)

    return embed


    
async def levelLeaderboard(p):
    global guild
    
    try:
        Database.cursor.execute("SELECT id, lvl, xp FROM Users ORDER BY xp DESC")
        users = Database.cursor.fetchall()
    except Exception as e:
        debug(type="lvlboard database", data=str(id), error=str(e))
        error_logging_to_guild(error=e)
    embed = disnake.Embed(title='ADTG XP Leaderboard, page ' + str(p + 1), color=0xdf8cfe)
        
    i = 0;
    i = i + 10 * p
    p = (p+1) * 10
    postition_count = i  
    
    while i < p and i < len(users):
        text = "Level: " + str(users[i][1]) + ", totale xp: " + str(users[i][2])
        if len(users) >=3:
            postition_count = postition_count + 1
            user_id = users[i][0]
            name = (await bot.get_or_fetch_user(user_id)).name             
            embed.add_field(name=f"#{postition_count} - {name}", value=text, inline=False)
        else:
            embed.add_field(name="Onbekend", value=text, inline=False)
        i = i + 1
    
    return embed



async def compLeaderboard(p):

    try:
        Database.cursor.execute("SELECT id, complements FROM Users ORDER BY complements DESC")
        result = Database.cursor.fetchall()
    except Exception as e:
        debug(type="compleaderboard database", data=str(id), error=str(e))
        error_logging_to_guild(error=e)

    embed = disnake.Embed(title='ADTG XP Levelbord, pagina ' + str(p + 1), color=0xdf8cfe)
    i = 0;
    i = i + 10 * p
    p = (p+1) * 10
    if i >= len(users):
        embed = disnake.Embed(title="Zoveel pagina's hebben we niet.", color=0xdf8cfe)
        return embed

    while i < p and i < len(users):

        text = "complimenten: " + str(users[i][1])
        if len(users) >=3:
            user_id = users[i][0]
            name = (await bot.get_or_fetch_user(user_id)).name 
            
            embed.add_field(name=name, value=text, inline=False)
        else:
            embed.add_field(name="Onbekend", value=text, inline=False)
        i = i + 1
    
    return embed



async def levelMessage(id):
    xp = get_xp(id)
    level = get_level(id)
    complements = get_complements(id)

    user = (await bot.get_or_fetch_user(id)).name
    user_avatar = (await bot.get_or_fetch_user(id)).avatar

    if xp == 0 and level == 0:
        embed = disnake.Embed(title="Er ging iets fout.", color=0xdf8cfe)
        embed.set_author(name=user, icon_url=user_avatar)
        return embed

    needed = int(8.196 * pow((level + 1), 2.65) + 200)
    needed = needed - xp

    embed = disnake.Embed(color=disnake.Color.green())
    embed.set_author(name=user, icon_url=user_avatar)
    
    embed.add_field(name="Huidig level:   ", value=str(level)+"   ", inline=True)
    embed.add_field(name="XP nodig:   ", value=str(needed)+"   ", inline=True)
    embed.add_field(name="Totale XP:   ", value=str(xp)+"   ", inline=True)
    embed.add_field(name="Complimenten:   ", value=str(complements), inline=True)

    return embed



def author_check(author):
    return lambda message: message.author == author



async def thank(inter, gebruiker, reden):
    global users
    if inter.author.id == gebruiker.id:
        
        e = disnake.Embed(title="Je kan jezelf niet bedanken, pannekoek!", color=0xdf8cfe)
        e.set_author(name=inter.author.name, icon_url=inter.author.avatar)
        e.add_field(name="Wat denk je nou joh", value="Mafklapper!")
        return e
    
    get_actual_daily_compliments = get_dailycomplements(inter.author.id)
    if get_actual_daily_compliments > 2:
        e = disnake.Embed(title="Je hebt niet genoeg complimenten over vandaag!", color=0xdf8cfe)
        e.set_author(name=inter.author.name) #, icon_url=m.author.avatar_url
        e.add_field(name="Complimenten over vandaag: ", value=get_actual_daily_compliments - 3, inline=True)
        e.add_field(name="Gecomplimenteerde users: ", value=get_actual_daily_compliments, inline=True)
        
    else:
        user = (await bot.get_or_fetch_user(gebruiker.id)).name
        
        set_dailycomplements(inter.author.id, get_actual_daily_compliments + 1)
        e = disnake.Embed(title="Complimenten", color=disnake.Color.green())
        e.set_author(name=inter.author.name, icon_url=inter.author.avatar)

        complements = get_complements(gebruiker.id)
        set_complements(gebruiker.id, complements + 1)
        gainXP(gebruiker.id, 150, 150)
        e.add_field(name="Compliment gegeven aan", value=user)
        e.add_field(name="Reden", value=reden)


    return e



def set_xp(id, xp):

    try:
        Database.cursor.execute("UPDATE Users SET xp = " + str(xp) + " WHERE id = " + str(id))
        Database.db.commit()
    except Exception as e:
        debug(type="set_xp database", data=str(id), error=str(e))
        error_logging_to_guild(error=e)



def get_xp(id):

        try:
            Database.cursor.execute("SELECT xp FROM Users WHERE id = " + str(id))
            result = Database.cursor.fetchone()[0]
            return result
        except Exception as e:
            debug(type="get_xp database", data=str(id), error=str(e))
            error_logging_to_guild(error=e)



def set_level(id, lvl):

    try:
        Database.cursor.execute("UPDATE Users SET lvl = " + str(lvl) + " WHERE id = " + str(id))
        Database.db.commit()
    except Exception as e:
        debug(type="set_level database", data=str(id), error=str(e))
        error_logging_to_guild(error=e)    



def get_level(id):
    Database.cursor.execute("SELECT lvl FROM Users WHERE id=" + str(id))
    if Database.cursor.rowcount == 0:
        return 0
    else:

        try:
            result = Database.cursor.fetchone()[0]
            return result

        except Exception as e:
            debug(type="get_level database", data=str(id, result), error=str(e))
            error_logging_to_guild(error=e)
            pass
    


def set_complements(id, complements):
    try:
        Database.cursor.execute("UPDATE Users SET complements = " + str(complements) + " WHERE id = " + str(id))
        Database.db.commit()
    except Exception as e:
        debug(type="set_complements database", data=str(id), error=str(e))
        error_logging_to_guild(error=e)



def get_complements(id):
    Database.cursor.execute("SELECT complements FROM Users WHERE id = " + str(id))
    if Database.cursor.rowcount == 0:
        return 0
    else:

        try:
            result = Database.cursor.fetchone()[0]
        except Exception as e:
            debug(type="get_complements database", data=str(id), error=str(e))
            error_logging_to_guild(error=e)
        return result



def set_dailycomplements(id, dailycomplements):

    try:
        Database.cursor.execute("UPDATE Users SET dailycomplements = " + str(dailycomplements) + " WHERE id = " + str(id))
        Database.db.commit()
    except Exception as e:
        error_logging_to_guild(error=e)
        debug(type="set_dailycomplements database", data=str(id), error=str(e))



def get_dailycomplements(id):

    Database.cursor.execute("SELECT dailycomplements FROM Users WHERE id = " + str(id))
    if Database.cursor.rowcount == 0:
        return 0
    else:
        try:
            result = Database.cursor.fetchone()[0]
        except Exception as e:
            debug(type="get_dailycomplements database", data=str(id), error=str(e))
            error_logging_to_guild(error=e)
        return result



def create_user(id, xp):

    try:
        Database.cursor.execute("INSERT INTO Users(id, xp, lvl, dailycomplements, complements) VALUES ("+ str(id) + ", " + str(xp) + ", 0, 0, 0);")
        Database.db.commit()
    except Exception as e:
        debug(type="create_user database", data=str(id), error=str(e))
        error_logging_to_guild(error=e)


def delete_user(id):

    try:
        Database.cursor.execute("DELETE FROM Users WHERE id = " + str(id))
        Database.db.commit()
    except Exception as e:
        debug(type="delete_user database", data=str(id), error=str(e))        
        error_logging_to_guild(error=e)



def Minute():
    global messaged
    global vChannels
    global users
    threading.Timer(60, Minute).start()
    messaged = []

    for vChannel in vChannels:
        channel = bot.get_channel(vChannel)
        if len(channel.members) > 1:
            for member in channel.members:
                if not(member.voice.afk or member.voice.mute or member.voice.deaf or member.voice.self_mute or member.voice.self_deaf):
                    gainXP(member.id, 4, 6)



# DEBUGGING
def debug(type, data, error):
    print(f"**Type:** {type} -- **Data:** {data} -- **Python exception:** {error}")



# validate users
def validate_user_in_db(id):
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
        error_logging_to_guild(error=e)
        pass
    


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



# Basic log function
def basic_log(log):
    channel_to_send = bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)

    embed=disnake.Embed(title="Adje log", description=str(log), color=disnake.Color.green())
    embed.set_footer(text=f"Datum: {str(datetime.now(tz_AM))[0:19]}")

    bot.loop.create_task(channel_to_send.send(embed=embed))



# Sending stuff to LOG channel
def error_logging_to_guild(error):
    channel_to_send = bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)

    embed=disnake.Embed(title="Adje log", description="Error", color=0xdf8cfe)
    embed.add_field(name=f"Error data:", value=str(error), inline=True)
    embed.set_footer(text=f"Datum: {str(datetime.now(tz_AM))[0:19]}")

    bot.loop.create_task(channel_to_send.send(embed=embed))



# Loading different cogs
bot.load_extension("cogs.ad_weer") 
bot.load_extension("cogs.forum") 
bot.load_extension("cogs.birthday") 
bot.load_extension("cogs.log_to_server") 
bot.load_extension("cogs.community") 
bot.load_extension("cogs.moderation") 
bot.load_extension("cogs.configuration") 
bot.load_extension("cogs.modmail") 



# Running the bot and starting thread
if __name__ == '__main__':
        bot.run(secure.BOT_TOKEN)