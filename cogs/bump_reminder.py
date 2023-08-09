import disnake
from disnake.ext import commands, tasks
from env import *
import time
from datetime import datetime, timedelta

class Bump_reminder(commands.Cog):


    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Bump reminder is loaded!")
        self.bumped_messages = []



    @commands.Cog.listener()
    async def on_ready(self):
        Bump_reminder.check_if_bump_is_ready.start(self)



    @tasks.loop(seconds=5)
    async def check_if_bump_is_ready(self):

        try:
            channel = self.bot.get_channel(Channel.ALLDAYBOT)
            messages_in_channel = await channel.history(limit=100).flatten()

            for message in messages_in_channel:
                if hasattr(message, "embeds"):
                    embeds = message.embeds
                    for embed in embeds:
                        try:
                            if "Check it out [on DISBOARD](https://disboard.org/server/716388937450389514)." in str(embed.description) and message.id not in self.bumped_messages:
                                datetime_object_message = datetime.strptime(str(message.created_at).split(".")[0], "%Y-%m-%d %H:%M:%S")                
                                datetime_object_now = datetime.strptime(str(datetime.now()).split(".")[0], "%Y-%m-%d %H:%M:%S")

                                time_difference = str(datetime_object_now - datetime_object_message - timedelta(hours=2)).split(":")[0]
                                
                                if time_difference == "2" or time_difference == "3":
                                    print("Bump ready!")
                                    await channel.send("De server kan weer gebumped worden! Dit kan d.m.v het command `/bump`. Dit helpt de server groeien!")
                                    self.bumped_messages.append(message.id)
                        except Exception as error:
                            print(error)
                            pass
        except Exception as error:
            print(error)
            pass


def setup(bot: commands.Bot):
    bot.add_cog(Bump_reminder(bot))