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
        self.lst_embeds_disboard = {}



    @commands.Cog.listener()
    async def on_ready(self):

        Bump_reminder.check_if_bump_is_ready.start(self)



    @tasks.loop(seconds=5)
    async def check_if_bump_is_ready(self):

        try: 
            # Getting bot channel
            channel = self.bot.get_channel(Channel.ALLDAYBOT)
            # Getting lastest 50 messages in channel
            for message in await channel.history(limit=50).flatten():
                
                # If message has embed and is from the Disboard bot
                if hasattr(message, "embeds") and message.author.id == 302050872383242240:
                    for embed in message.embeds:
                            # If message is from bumping and message isnt in list
                            if "Check it out [on DISBOARD]" in str(embed.description) and message.id not in self.bumped_messages:
                                # Make time object from message time (and removing micro seconds)
                                msg_time_object = datetime.strptime(str(message.created_at).split(".")[0], "%Y-%m-%d %H:%M:%S") + timedelta(hours=2)
                                time_now = datetime.strptime(str(datetime.now()).split(".")[0], "%Y-%m-%d %H:%M:%S")
                                seconds_difference = time_now - msg_time_object
                                
                                # If seconds difference are between 2 hour and 2 hour and 10 seconds
                                if int(seconds_difference.seconds) >= 7200 and int(seconds_difference.seconds) < 7210:
                                    print("DEBUG 1 bump: ", msg_time_object)
                                    print("DEBUG 2 bump: ", time_now)
                                    print("Server is ready to be bumped!")
                                    #await channel.send("De server kan weer gebumped worden! Dit kan d.m.v het command `/bump`. Dit helpt de server groeien!")
                                    self.bumped_messages.append(int(message.id)) 

        except Exception as error:
            print(error)
            pass



def setup(bot: commands.Bot):
    bot.add_cog(Bump_reminder(bot))