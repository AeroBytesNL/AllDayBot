import disnake
from disnake.ext import commands, tasks
from env import *
from database import *



intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)



@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing , name="DM om beheer te contacteren"))
    print("The bot is ready!")



@tasks.loop(seconds=120) 
async def keep_sql_active():
    Database.cursor.execute("SELECT * FROM Users WHERE id='632677231113666601'")
    res = Database.cursor.fetchone()
    print("Just keeping the data-slut active!")
    
keep_sql_active.start()


            
# Loading different cogs
bot.load_extension("cogs.ad_weer") 
bot.load_extension("cogs.forum") 
bot.load_extension("cogs.birthday") 
bot.load_extension("cogs.log_to_server") 
bot.load_extension("cogs.community") 
bot.load_extension("cogs.moderation") 
bot.load_extension("cogs.modmail") 
#bot.load_extension("cogs.minecraft") 
bot.load_extension("cogs.leveling") 
bot.load_extension("cogs.it_admin") 
bot.load_extension("cogs.buy_sell") 
bot.load_extension("cogs.news") 
bot.load_extension("cogs.announce") 
bot.load_extension("cogs.analytics") 



# Running the bot and starting thread
if __name__ == '__main__':
        bot.run(secure.BOT_TOKEN)