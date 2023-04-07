import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
from env import *
from database import *
from datetime import datetime, date
from dateutil import relativedelta
import re
from typing import Optional





class modmail(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # On DM
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user or message.author.bot:
            return        
        
        if isinstance(message.channel, disnake.channel.DMChannel):
            await modmail.first_contact(self, message)


    class Confirm(disnake.ui.View):
        def __init__(self):
            super().__init__(timeout=10.0)
            self.value: Optional[bool] = None

        # When the confirm button is pressed, set the inner value to `True` and
        # stop the View from listening to more input.
        # We also send the user an ephemeral message that we're confirming their choice.
        @disnake.ui.button(label="Confirm", style=disnake.ButtonStyle.green)
        async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
            await inter.response.send_message("Confirming...")
            self.value = True
            self.stop()

        # This one is similar to the confirmation button except sets the inner value to `False`.
        @disnake.ui.button(label="Cancel", style=disnake.ButtonStyle.grey)
        async def cancel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
            await inter.response.send_message("Cancelling...")
            self.value = False
            self.stop()


    # Functions
    async def first_contact(self, message):
        view = self.Confirm()
        print(message.author.name)
        
        embed=disnake.Embed(title=f"ModMail", description=f"Verzoek", color=disnake.Color.orange())
        embed.add_field(name="Vraag:", value=str(message.clean_content), inline=False)
        await message.channel.send(embed=embed, view=view)


        await view.wait()

        if view.value is None:
            print("Timed out.")
        elif view.value:
            guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
            category = disnake.utils.get(guild.categories, name="test")
            await guild.create_text_channel(name="{message.author.nick}-modmail", category=category)   
        else:
            print("Cancelled.")


     



def setup(bot: commands.Bot):
    bot.add_cog(modmail(bot))