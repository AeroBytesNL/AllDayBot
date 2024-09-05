import disnake
from disnake.ext import commands
from env import AntiBot as AntiBotEnv

class AntiBot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog anti_bot is loaded!")

    @commands.Cog.listener()
    async def on_raw_member_update(self, member):
        for role in member.roles:
            if role.id == AntiBotEnv.ANTI_BOT_ROLE_ID:
                user = self.bot.get_user(member.id)
                await user.send("""
                                Je bent gekicked uit All Day Tech & Gaming omdat je de automatische bot-preventie rol hebt geselecteerd. 
                                Je kan opnieuw lid worden via onze uitnodigingslink. 
                                Mocht je geen toegang hebben tot deze link, stuur dan een bericht naar deze bot om contact te leggen met het beheer voor een uitnodigingslink.
                                """)
                await user.kick(reason="Gebruiker eruit YEET ivm het selecteren van de anti bot rol (automatisch)")
                print("AllDayAntiBot kicked an user because he selected the anti bot role!")

def setup(bot: commands.Bot):
    bot.add_cog(AntiBot(bot))