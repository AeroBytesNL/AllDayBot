import disnake
from disnake.ext import commands, tasks
from env import *
from database import *
from helpers.ntfy import NtfyLogging
import sentry_sdk
from helpers.error import Log

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)

sentry_sdk.init(
    dsn=Sentry.DSN,
)

@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.playing , name="DM om beheer te contacteren"))
    Log.info(f"Signed in as {bot.user.name}")
    Log.info(f"The bot is Ready!")

@tasks.loop(seconds=120) 
async def keep_sql_active():
    try:     
        Database.cursor.execute("SELECT * FROM Users WHERE id='632677231113666601'")
        Database.cursor.fetchone()
        Log.info("Keeping the database aka dataslut active")
    except Exception as error:
        Log.error(f"keep_sql_active {error}")
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

# Running the bot
if __name__ == '__main__':
        bot.run(secure.BOT_TOKEN)