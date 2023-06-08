import disnake
from disnake.ext import commands, tasks
from disnake.enums import ButtonStyle
from env import *
from database import Database
from datetime import datetime
import pytz

# TODO change month string to int

class buy_sell(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog buy/sell is loaded!")
        buy_sell.buy_sell_cleaner_9000.start(self)

    # making loop
    # TODO change to 240 minutes
    @tasks.loop(seconds=1) 
    async def buy_sell_cleaner_9000(self):
        print("Running ")
        try:
            buy_sell_channel = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)

            messages = await buy_sell_channel.history(limit=200).flatten()
            
            for message in messages:
                print(message)

        except Exception as error:
            print(error)
                
            

def setup(bot: commands.Bot):
    bot.add_cog(buy_sell(bot))                    
