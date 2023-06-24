import disnake
from disnake.ext import commands
from env import *
from database import *



class Reminder(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Reminder is loaded!")
        self.cache = []


    # Mother Off All Commands
    @commands.slash_command()
    async def reminder(self, inter):
        pass


    # Server commands
    @reminder.sub_command(description="Voeg een reminder toe")
    async def toevoegen(self, inter, tijd:str, reden:str):
        
        try:
            # CODE HIERO
            if ":" in tijd:
                i = tijd.split(":")
                print(i)
            else:
                print(tijd)

            # INSERT into db
            # Empty cache
            await Reminder.insert_time_in_db(inter=inter, time=tijd, reason=reden)
            self.cache = ()

        except Exception as error:
            await inter.response.send_message(f"Error: {error}")



    @reminder.sub_command(description="get")
    async def get_data(self, inter):
        
        try:
            await Reminder.get_times_from_db(self=self)

        except Exception as error:
            await inter.response.send_message(f"Error: {error}")



    async def insert_time_in_db(inter, time, reason):
        Database.cursor.execute(f"INSERT INTO reminder (user_id, time, reason) VALUES ('{inter.author.id}', '{time}', '{reason}')")
        Database.db.commit()


    
    async def get_times_from_db(self):
        
        # cache 
        lenght_cache = len(self.cache)

        print(lenght_cache)

        # If cache is full
        if lenght_cache != 0:
            print(self.cache)
            print("In cache")
            return self.cache[0]


        # if cache isnt full
        if lenght_cache == 0:
            Database.cursor.execute("SELECT user_id, time, reason FROM reminder")
            res = Database.cursor.fetchall()[0]
            self.cache.append(res)

            print(self.cache)
            print("Not in cache")
            return self.cache[0]
        

def setup(bot: commands.Bot):
    bot.add_cog(Reminder(bot))