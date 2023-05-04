import disnake
from disnake.ext import commands, tasks
from disnake import TextInputStyle

from env import *
from database import Database


class Configuration(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Configuration is loaded!")



        @commands.default_member_permissions(administrator=True)
        @bot.slash_command()
        async def config(inter):
            pass


        @config.sub_command(description="Verander de pc-advies tekst")
        async def pc_advies_tekst(self, inter):
            await inter.response.send_message(modal=Configuration.Modal(fields=("1","3", "4", "5", "6")))




    # Modal main
    class Modal(disnake.ui.Modal):
        def __init__(self, fields):
            
            components = []

            if len(fields) > 1:
                for value in fields:
                    print(value)
                    components.append(
                        label=str(value[1]),
                        placeholder=str[value[2]],
                        custom_id=str(value[3]),
                        style=value[4],
                        max_length=int(value[5]),
                    )

            else:
                components.append(
                    label=str(value[1]),
                    placeholder=str[value[2]],
                    custom_id=str(value[3]),
                    style=value[4],
                    max_length=int(value[5]),
                
                )
                
            super().__init__(title=str(value[0]), components=components)

            async def callback(self, inter: disnake.ModalInteraction):
                await inter.response.send_message("Je bericht is gewijzigd!", ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(Configuration(bot))