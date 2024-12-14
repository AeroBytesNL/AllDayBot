import disnake
from disnake.ext import commands
from env import AntiBot as AntiBotEnv
from env import env_variable
from helpers.error import Log

class AntiBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Loaded Cog anti_bot")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        for role in after.roles:
            if role.id == AntiBotEnv.ANTI_BOT_ROLE_ID:
                user = await self.bot.fetch_user(after.id)
                guild = await self.bot.fetch_guild(env_variable.GUILD_ID)

                await user.send("""
                                Je bent gekicked uit All Day Tech & Gaming omdat je de automatische bot-preventie rol hebt geselecteerd. 
                                Je kan opnieuw lid worden via onze uitnodigingslink. 
                                Mocht je geen toegang hebben tot deze link, stuur dan een bericht naar deze bot om contact te leggen met het beheer voor een uitnodigingslink.
                                """)
                await guild.kick(user=after, reason="Gebruiker eruit geyeet ivm het selecteren van de anti bot rol (automatisch)")
                print("AllDayAntiBot kicked an user because he selected the anti bot role!")

def setup(bot: commands.Bot):
    bot.add_cog(AntiBot(bot))