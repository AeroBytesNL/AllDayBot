import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database
from time import sleep

class User_saver(commands.Cog):



    def __init__(self, bot: commands.Bot):

        self.bot = bot
        print("Cog User saver is loaded!")
        self.user_saver_9000.start()
    


    @tasks.loop(seconds=60)
    async def user_saver_9000(self):
        user_db_dict = {}

        users_to_insert_in_db = {}
        users_to_update_username = {}

        for user in User_saver.get_users_from_db():
            user_db_dict[user[0]] = str(user[1])
        
        try:

            guild = self.bot.get_guild(env_variable.GUILD_ID)
            
            for user in guild.members:
                
                if user.id not in user_db_dict:
                    users_to_insert_in_db[user.id] = str(user.name)
                
                if user.id in user_db_dict and user_db_dict.get(user.id) != user.name:
                    users_to_update_username[user.id] = str(user.name)

            User_saver.insert_user_in_db(users_to_insert_in_db)
            User_saver.update_username_in_db(users_to_update_username)

        except Exception as error:
            print(error)
            pass

    

    def get_users_from_db():
        Database.cursor.execute("SELECT * FROM user_saver")
        return Database.cursor.fetchall()



    def insert_user_in_db(users_to_insert_in_db):
        
        for user in users_to_insert_in_db:
            user_name = users_to_insert_in_db.get(user)
            Database.cursor.execute(f"INSERT INTO user_saver (user_id, user_name) VALUES ({user}, '{user_name}')")

        Database.db.commit()


    
    def update_username_in_db(users_to_update_username):

        for user in users_to_update_username:
            user_name = users_to_update_username.get(user)
            Database.cursor.execute(f"UPDATE user_saver SET user_name='{user_name}' WHERE user_id={user}")

        Database.db.commit()



def setup(bot: commands.Bot):
    bot.add_cog(User_saver(bot))