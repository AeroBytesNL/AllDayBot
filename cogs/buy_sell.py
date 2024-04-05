import disnake
from disnake.ext import commands, tasks
from database import Database
import datetime
from env import *


class Buy_sell(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Buy_sell.not_selled_articles.start(self)
        print("Cog buy_sell is loaded!")


    @tasks.loop(seconds=5)
    async def not_selled_articles(self):
        try:
            guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
            channel = await self.bot.fetch_channel(Channel.BUY_SELL)
            active_threads = await guild.active_threads()
            archived_threads = channel.archived_threads()

            for archived_thread in archived_threads:
                print(archived_thread.name)

        except Exception as error:
            print(error)
            pass


    # Called when a new thread is created
    # If in the buy sell forum, insert data into DB
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent_id != 1179111617196216361: return
        
        Buy_sell.insert_thread_into_db(self, thread)
        

    # Called when a thread is deleted
    # If in the buy sell forum, delete data from DB
    @commands.Cog.listener()
    async def on_raw_thread_delete(self, payload):
        if payload.parent_id != 1179111617196216361: return

        Buy_sell.delete_thread_from_db(self, payload)	


    def insert_thread_into_db(self, thread):
        Database.cursor.execute(f"INSERT INTO koop_verkoop (archived, auto_archive_duration, create_timestamp, thread_id, owner_id) VALUES (0, {thread.auto_archive_duration}, '{thread.create_timestamp}', {thread.id}, {thread.owner_id})")
        Database.db.commit()


    def delete_thread_from_db(self, payload):
        Database.cursor.execute(f"DELETE FROM koop_verkoop WHERE thread_id={payload.thread_id}")
        Database.db.commit()


    def get_threads_from_db():
        Database.cursor.execute("SELECT * FROM koop_verkoop")
        return Database.cursor.fetchall()
    

def setup(bot: commands.Bot):
    bot.add_cog(Buy_sell(bot))                    
