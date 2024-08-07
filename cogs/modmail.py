import disnake
from disnake.ext import commands
from env import *
from database import *

# TODO change user.name to general name to prefend errors
class modmail(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog ModMail is loaded!")


    # On message
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return        
    
        # if message is in DM
        if isinstance(message.channel, disnake.channel.DMChannel):
            i = True
            for guild in self.bot.guilds:
                for channel in guild.threads:
                    if f"{message.author.name}&&MM" == str(channel.name):
                        await modmail.send_user_response(self, message, thread_to_send=channel)
                        i = False
                    else:
                        pass

            # Sending embed with the question
            if i != True:
                return
            
            await modmail.handle_first_contact(self, message)
            return

        # if message is in a thread
        if hasattr(message, "thread"):
            if not isinstance(message.channel, disnake.channel.DMChannel):
                if "MM" in str(message.channel.name):
                    username_to_send = str(message.channel.name).split("&&")[0]
                    for member in self.bot.get_all_members():
                        if member.name == username_to_send:
                            await modmail.send_admin_response_to_ticket_maker(self, message, member)
                            await modmail.close_ticket_and_thread(self, message, member)


    # Handles when an user sends an message to the bot
    # Sends embed back to the user if he wants to send the message
    # If yes, make thread
    # Else, do nothing
    async def handle_first_contact(self, message):
        class Confirm(disnake.ui.View):

            def __init__(self):
                super().__init__(timeout=0)

            @disnake.ui.button(label="Verstuur", style=disnake.ButtonStyle.green)
            async def confirm(self_inside_button, button: disnake.ui.Button, inter: disnake.MessageInteraction):
                await inter.response.send_message("Ik heb het verstuurd!")
                # Starting make thread
                modmail_channel = self.bot.get_channel(env_variable.MODMAIL_ID)
                await modmail_channel.create_thread(
                    name = f"{inter.author.display_name} - ModMail ticket",
                    auto_archive_duration=0,
                    message='jo'
                )
                self_inside_button.stop()

            @disnake.ui.button(label="Annuleer", style=disnake.ButtonStyle.grey)
            async def cancel(self_inside_button, button: disnake.ui.Button, inter: disnake.MessageInteraction):
                await inter.response.send_message("Ik heb het geannuleert!")
                self_inside_button.stop()

        view = Confirm()

        user = await self.bot.fetch_user(message.author.id)

        # send embed back to confirm message
        embed = disnake.Embed(
            title = "Contacteer ADT&G beheer",
            description = "Wil je het volgende bericht versturen?",
            color = disnake.Colour.blue()
        )

        embed.add_field(
            name = message.content,
            value= "\n"
        )

        await user.send(
            embed=embed, 
            view=view
        )

def setup(bot: commands.Bot):
    bot.add_cog(modmail(bot))