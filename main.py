import disnake
from disnake.ext import commands, tasks
from env import *
from database import *
import sentry_sdk
from helpers.error import Log

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)

sentry_sdk.init(
    dsn=Sentry.DSN,
)

@bot.event
async def on_ready():
    try:
        await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing , name="DM om beheer te contacteren"))
        Log.info(f"Signed in as {bot.user.name}")
    except Exception as error:
        Log.error(f"Error while signing in: {error}`")

@tasks.loop(seconds=120) 
async def keep_sql_active():
    try:
        Log.debug("Running task \"keep_sql_active\"")
        Database.cursor.execute("SELECT * FROM Users WHERE id='632677231113666601'")
        Database.cursor.fetchone()
        Log.debug("Task \"keep_sql_active\" has finished")
    except Exception as error:
        Log.error(f"Error while running task \"keep_sql_active\": {error}")
        pass
    
keep_sql_active.start()

bot.load_extension("cogs.ad_weer")
bot.load_extension("cogs.forum") 
bot.load_extension("cogs.birthday") 
bot.load_extension("cogs.log_to_server") 
bot.load_extension("cogs.community") 
bot.load_extension("cogs.moderation") 
bot.load_extension("cogs.modmail") 
#bot.load_extension("cogs.minecraft") 
bot.load_extension("cogs.leveling") 
bot.load_extension("cogs.buy_sell")
bot.load_extension("cogs.news") 
bot.load_extension("cogs.announce") 
bot.load_extension("cogs.analytics") 
#bot.load_extension("cogs.test") 
bot.load_extension("cogs.website")
bot.load_extension("cogs.quiz")
bot.load_extension("cogs.bump")
bot.load_extension("cogs.introduce_remover")
bot.load_extension("cogs.welcome_message")
bot.load_extension("cogs.showcase_remover")
bot.load_extension("cogs.anti_bot")
bot.load_extension("cogs.status")
bot.load_extension("cogs.llm")
#bot.load_extension("cogs.custom_invite")
bot.load_extension("cogs.invite_tracker")

if __name__ == '__main__':
    bot.run(secure.BOT_TOKEN)