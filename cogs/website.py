import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database
import secrets



class Website(commands.Cog):



    def __init__(self, bot: commands.Bot):

        self.bot = bot
        print("Cog Website is loaded!")



    @commands.slash_command()
    async def website(self, inter):
        pass



    @website.sub_command(description="Maak een account aan op de ADB site")
    async def account_maken(self, inter):
        
        token = secrets.token_hex(10)
        Website.insert_token_in_db(token)
        print(f"User {inter.author.name} made a adb website account creation code")
        await inter.response.send_message(f"Je kunt een account maken d.m.v de volgende link: https://alldaybot.alldaytechandgaming.nl/account-maken-token/{token}", ephemeral=True)


    def insert_token_in_db(token):
        Database.cursor.execute(f"INSERT INTO account_creation_tokens (token) VALUES ('{token}')")
        Database.db.commit()



def setup(bot: commands.Bot):
    bot.add_cog(Website(bot))   