import disnake
from disnake.ext import commands, tasks
from env import *
from database import *



class Reminder(commands.Cog):
    
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_saver.start()
        print("Cog User saver is loaded!")



    @tasks.loop(seconds=60)
    async def user_saver(self):
        print("debugg")

        # Getting guild and users
        guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
        members = await guild.fetch_members(limit=2000).flatten()

        # Getting current member list
        Database.cursor.execute("SELECT * FROM guild_users")
        res = Database.cursor.fetchall()

        user_id_in_db = []

        for entry in res:
            user_id_in_db.append(int(entry[0]))

        for user in members:
            if user.id not in user_id_in_db:
                Database.cursor.execute(f"INSERT INTO guild_users (user_id, user_display_name, user_name, created_at, joined_at) VALUES ({user.id}, '{user.display_name}', '{user.name}', '{str(user.created_at).split('.')[0]}', '{str(user.joined_at).split('.')[0]}')")
                Database.db.commit()


def setup(bot: commands.Bot):
    bot.add_cog(Reminder(bot))