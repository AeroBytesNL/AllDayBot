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



intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing , name="DM om beheer te contacteren"))
    print("The bot is ready!")


            
# Loading different cogs
bot.load_extension("cogs.ad_weer") 
bot.load_extension("cogs.forum") 
bot.load_extension("cogs.birthday") 
bot.load_extension("cogs.log_to_server") 
bot.load_extension("cogs.community") 
bot.load_extension("cogs.moderation") 
bot.load_extension("cogs.modmail") 
bot.load_extension("cogs.minecraft") 
bot.load_extension("cogs.pc_text") 
#bot.load_extension("cogs.configuration") 
bot.load_extension("cogs.leveling") 



# Running the bot and starting thread
if __name__ == '__main__':
        bot.run(secure.BOT_TOKEN)