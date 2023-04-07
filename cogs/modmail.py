import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
from env import *
from database import *
from datetime import datetime, date
from dateutil import relativedelta
import re
from typing import Optional


# TODO add admin mention when thread created
# TODO change user.name to general name to prefend errors
# TODO if thread deleted, remove also "Nieuwe ModMail ticket"
# TODO fix "afwijzen" button

class modmail(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        


    # On message
    @commands.Cog.listener()
    async def on_message(self, message):


        # Cancels if message did come from a bot
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
            if i == True:
                await modmail.first_contact(self, message)
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


        

    # First contact
    async def first_contact(self, message):
        
        # Button class
        class Confirm(disnake.ui.View):

            @disnake.ui.button(label="Verstuur", style=disnake.ButtonStyle.green)
            async def confirm(self_inside_button, button: disnake.ui.Button, inter: disnake.MessageInteraction):
                await inter.response.send_message("Ik heb het verstuurd!")
                # Starting make thread function
                await modmail.create_contact_with_staff(self, message)
                self_inside_button.stop()

            @disnake.ui.button(label="Annuleer", style=disnake.ButtonStyle.grey)
            async def cancel(self_inside_button, button: disnake.ui.Button, inter: disnake.MessageInteraction):
                await inter.response.send_message("Ik heb het geannuleert!")
                self_inside_button.stop()

        # Creating instance
        view = Confirm()

        # Embed
        embed=disnake.Embed(title="Contact ADT&G beheer", description="\n", color=disnake.Color.green())
        embed.add_field(name=f"Vraag:", value=str(message.clean_content), inline=True)
        await message.channel.send(embed=embed, view=view)



    # Making thread
    async def create_contact_with_staff(self, message):

        # Button class
        class Confirm(disnake.ui.View):

            @disnake.ui.button(label="Accepteren", style=disnake.ButtonStyle.green)
            async def confirm(self_inside_button, button: disnake.ui.Button, inter: disnake.MessageInteraction):
                await inter.response.send_message("Ik heb het verzoek geaccepteert!")
                # Starting make thread function
                await modmail.accept_or_deny(self, message, type=True, by_user=inter.author.name)
                self_inside_button.stop()

            @disnake.ui.button(label="Afwijzen", style=disnake.ButtonStyle.grey)
            async def cancel(self_inside_button, button: disnake.ui.Button, inter: disnake.MessageInteraction):
                msg = await inter.response.send_message("Ik heb het verzoek afgewezen!")
                thread_to_close= self.bot.get_channel(inter.channel.id)
                
                await thread_to_close.delete(reason=f"Ticket gesloten door `{inter.author.name}`")

                await modmail.accept_or_deny(self, message, type=False, by_user=inter.author.name)
                await modmail.remove_last_msg(self)
                self_inside_button.stop()

        # Creating instance
        view = Confirm()

        # Get admin and mod roles
        guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
        role_admin = guild.get_role(Role_ids.ADMIN)
        role_moderator = guild.get_role(Role_ids.MODERATOR)

        channel = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        msg = await channel.send(f"Nieuwe ModMail ticket {role_admin.mention}, {role_moderator.mention}", allowed_mentions=disnake.AllowedMentions(roles=True))
        thread  = await channel.create_thread(name=f"{str(message.author.name)}&&MM", reason=f"ModMail for {message.author.name}", type=None, message=msg)

        # Embed 
        embed=disnake.Embed(title="Contact ADT&G beheer", description=f"Van user: {message.author.name}", color=disnake.Color.red())
        embed.add_field(name=f"Vraag:", value=str(message.clean_content), inline=True)
        await thread.send(embed=embed, view=view)

        

    # Deny or accept request from user
    async def accept_or_deny(self, message, type, by_user):
            
        if type == True:
            embed=disnake.Embed(title="Contact ADT&G beheer", description=f"Verzoek geaccepteerd door `{by_user}`! Het kan even duren voor je antwoord krijgt.", color=disnake.Color.green())
        else:
            embed=disnake.Embed(title="Contact ADT&G beheer", description=f"Verzoek geweigerd door `{by_user}`! Probeer het anders opnieuw met een betere vraag.", color=disnake.Color.red())
        
        await message.channel.send(embed=embed)



    # Sending response from ticket handler to end user
    async def send_admin_response_to_ticket_maker(self, message, member):
        embed=disnake.Embed(title=f"Contact ADT&G antwoord", description=f"Door beheerder: `{message.author.name}`", color=disnake.Color.green())
        embed.add_field(name=f"Antwoord beheer:", value=str(message.clean_content), inline=False)
        embed.add_field(name=f"\n", value="Als je vraag niet beantwoord is, dan kun je hieronder gewoon terugtypen! (In 1 bericht)", inline=False)

        await member.send(embed=embed)



    # Closing thread
    async def close_ticket_and_thread(self, message, member):
        # Button class
        class Confirm(disnake.ui.View):

            @disnake.ui.button(label="Close ticket", style=disnake.ButtonStyle.red)
            async def confirm(self_inside_button, button: disnake.ui.Button, inter: disnake.MessageInteraction):
                
                await inter.response.send_message("Ik heb de ticket gesloten!")
                embed=disnake.Embed(title="Contact ADT&G ticket gesloten!", description=f"Door: `{message.author.name}`", color=disnake.Color.red())
                await member.send(embed=embed)
                
                thread_to_close= self.bot.get_channel(message.channel.id)
                await thread_to_close.delete(reason=f"Ticket beantwoord van {member.name}. Gesloten door `{inter.author.name}`")
                await modmail.remove_last_msg(self)
                self_inside_button.stop()

        # Creating instance
        view = Confirm()        

        embed=disnake.Embed(title="Je hebt dit gestuurd:", description=str(message.clean_content), color=disnake.Color.green())
        await message.channel.send(embed=embed, view=view)
    


    async def send_user_response(self, message, thread_to_send):
        embed=disnake.Embed(title="User reageerde:", description=str(message.clean_content), color=disnake.Color.red())
        await thread_to_send.send(embed=embed)



    # Log modmail actions to LOG channel
    async def logging(self, from_user, interaction, on_user):
        print(from_user, interaction, on_user)



    async def remove_last_msg(self):
        msg = (await self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID).history(limit=1).flatten())[0]
        if "Nieuwe ModMail" in str(msg.clean_content):
            await msg.delete()



def setup(bot: commands.Bot):
    bot.add_cog(modmail(bot))