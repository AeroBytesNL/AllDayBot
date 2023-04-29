import disnake
from disnake.ext import commands, tasks
from datetime import timedelta
from env import *
from database import *

bot = commands.Bot(intents=(disnake.Intents.all()))

@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing , name="DM om beheer te contacteren"))


# Loading different cogs
bot.load_extension("cogs.ad_weer") 
bot.load_extension("cogs.forum") 
bot.load_extension("cogs.birthday") 
bot.load_extension("cogs.log_to_server") 
bot.load_extension("cogs.community") 
bot.load_extension("cogs.moderation") 
bot.load_extension("cogs.modmail") 
bot.load_extension("cogs.minecraft") 
bot.load_extension("cogs.leveling") 


# Running the bot and starting thread
if __name__ == '__main__':
        bot.run(secure.BOT_TOKEN)