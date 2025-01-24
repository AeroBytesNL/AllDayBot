import disnake
from disnake.ext import commands, tasks
from env import *
import time
from datetime import datetime, timedelta, timezone
from database import Database
from helpers.error import Log

class Bump_reminder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_processed_bump = 0
        Log.info("Loaded Cog bump")

    @commands.Cog.listener()
    async def on_ready(self):
        Bump_reminder.check_if_bump_is_ready.start(self)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.channel.id != Channel.BUMP:
                return

            if message.author.id != 302050872383242240:
                return

            if message.interaction.name != "bump":
                return

            Bump_reminder.add_xp_to_bumper(self, message.interaction.user.id)
            Log.info("Added xp to bumper")

        except Exception as error:
            Log.error(error)
            pass

    @tasks.loop(seconds=5)
    async def check_if_bump_is_ready(self):
        try:
            messages = [
                msg for msg in await (await self.bot.fetch_channel(Channel.BUMP)).history(limit=50).flatten()
                if msg.interaction and msg.interaction.name == "bump"
            ]

            last_bump = max(messages, key=lambda x: x.id)

            if last_bump.id == self.last_processed_bump: return

            bump_time = last_bump.created_at
            diff = (datetime.now(timezone(timedelta(hours=1))) - bump_time).total_seconds()

            if diff >= 7192 and diff < 7200: 
                await (await self.bot.fetch_channel(Channel.BUMP)).send("De server kan weer gebumped worden! Dit kan d.m.v. het command `/bump`. Dit helpt de server groeien! (Ook ontvang je een bonus van 60 XP!)")
                Log.info("Server is ready to be bumped")
                self.last_processed_bump = last_bump.id

        except Exception as error:
            Log.error(error)
            pass

    def add_xp_to_bumper(self, author_id):
        try:
            Database.cursor.execute(f"SELECT xp FROM Users WHERE id='{author_id}'")
            res = Database.cursor.fetchone()[0]

            Database.cursor.execute(f"UPDATE Users SET xp = {res + 60} WHERE id='{author_id}'")
            Database.db.commit()
        except Exception as error:
            Log.error(error)
            pass

def setup(bot: commands.Bot):
    bot.add_cog(Bump_reminder(bot))
