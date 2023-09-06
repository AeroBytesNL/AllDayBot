import disnake
from disnake.ext import commands, tasks
from env import *
from datetime import datetime
import pytz
import numpy as np
from database import Database
import random



class announce(commands.Cog):



    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog announce is loaded!")



    # Commands aanounce admin
    @commands.default_member_permissions(moderate_members=True)
    @commands.slash_command(description="Verstuur een announcement naar een kanaal!")
    async def announce(self, inter, channel: disnake.TextChannel):
        
                
        class MyModal(disnake.ui.Modal):
            def __init__(custom_self_modal) -> None:
                components = [
                    disnake.ui.TextInput(
                        label="Content",
                        placeholder="Vul hier de aankondiging in",
                        custom_id="content",
                        style=disnake.TextInputStyle.paragraph,
                        min_length=5,
                        max_length=4000,
                    ),
                ]
                super().__init__(title="Aankondiging", custom_id="create_tag", components=components)

            async def callback(custom_self_modal, inter: disnake.ModalInteraction):
                
                content = inter.text_values["content"]
                print(content)

                guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
        
                embed=disnake.Embed(title="\n", description=str(inter.text_values["content"]), color=0xdf8cfe)
                embed.set_footer(text=f"Deze aankondiging is gemaakt door {inter.author.name}")
                embed.set_thumbnail(url=guild.icon)
                await channel.send(embed=embed)
                
                await inter.response.send_message("Aankondiging is verstuurd!", ephemeral=True)


        await inter.response.send_modal(modal=MyModal())


def setup(bot: commands.Bot):
    bot.add_cog(announce(bot))