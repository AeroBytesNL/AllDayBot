import disnake
from disnake.ext import commands, tasks
from env import *
import time
from datetime import datetime, timedelta
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
            # Get the bot channel
            channel = self.bot.get_channel(Channel.BUMP)

            # Find the last bump
            messages = list(
            filter(
                lambda x: x.interaction is not None and x.interaction.name == "bump", 
                await channel.history(limit=50).flatten()
            )
            )
            last_bump = max(messages, key=lambda x: x.id)

            # Check if we've already processed this bump
            if last_bump.id == self.last_processed_bump: return

            # Check if the last bump happened more than 2 hours ago
            bump_time = datetime.fromtimestamp(((last_bump.id >> 22) + 1420070400000) / 1000.0)
            diff = int((datetime.now() - bump_time).seconds)

            if diff >= 7192 and diff < 7200: 
                # Send the reminder
                await channel.send("De server kan weer gebumped worden! Dit kan d.m.v. het command `/bump`. Dit helpt de server groeien! (Ook ontvang je een bonus van 60 XP!)")
                Log.info("Server is ready to be bumped")
                self.last_processed_bump = last_bump.id

        except Exception as error:
            Log.error(error)
            pass

    def add_xp_to_bumper(self, author_id):
        Database.cursor.execute(f"SELECT xp FROM Users WHERE id='{author_id}'")
        res = Database.cursor.fetchone()[0]

        Database.cursor.execute(f"UPDATE Users SET xp = {res + 60} WHERE id='{author_id}'")
        Database.db.commit()

def setup(bot: commands.Bot):
    bot.add_cog(Bump_reminder(bot))
