import disnake
from disnake.ext import commands, tasks
from env import *
from datetime import datetime


class buy_sell(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog buy/sell is loaded!")
        buy_sell.buy_sell_cleaner_9000.start(self)


    @tasks.loop(seconds=360) 
    async def buy_sell_cleaner_9000(self):
        print("Doing an #koopverkoop scan")

        try:
            buy_sell_channel = self.bot.get_channel(env_variable.KOOP_VERKOOP_ID)
            messages = await buy_sell_channel.history(limit=200).flatten()
            
            for message in messages:
                splitted_string_datetime = str(message.created_at).split(".")[0]

                date_object = datetime.strptime(splitted_string_datetime, "%Y-%m-%d %H:%M:%S")
                date_diff = datetime.now().date() - date_object.date()

                if date_diff.days > 31 and message.author != self.bot.user:
                    await message.delete()
                    print("Message in buy sell deleted")

        except Exception as error:
            print(error)
                
            
def setup(bot: commands.Bot):
    bot.add_cog(buy_sell(bot))                    
