import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
from env import *
from database import *



class it_admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog it_admin is loaded!")


    # Check role
    async def role_checking_it(self, inter):

        guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
        role = disnake.utils.get(guild.roles, name="ServerDeveloper") 

        if not role in inter.author.roles:
            return False
        else:
            return True
    

    # Commands pc
    @commands.slash_command()
    async def it_management(self, inter):
        pass


    # advice
    @it_management.sub_command(description = "Edit de xp van een user in de DB")
    async def db_edit(self, inter, snowflake, xp_amount, level):
        x = await it_admin.role_checking_it(self, inter)
        print(x)
        if not await it_admin.role_checking_it(self, inter):
            await inter.response.send_message("Je bent geen IT beheer, sorry!", ephemeral=True)
        else:
            Database.cursor.execute(f"UPDATE Users SET xp={xp_amount}, lvl={level} WHERE id={snowflake}")
            Database.db.commit()
            await inter.response.send_message("Gelukt!", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(it_admin(bot))