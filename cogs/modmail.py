import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
from env import *
from database import *
from datetime import datetime, date
from dateutil import relativedelta


# TODO change user.name to general name to prefend errors

class modmail(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog ModMail is loaded!")


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
        class Confirm(disnake.ui.View):

            def __init__(self):
                super().__init__(timeout=0)

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

        view = Confirm()

        if message.attachments:
            embed=disnake.Embed(title="Contact ADT&G beheer", description="Wil je dit versturen?", color=disnake.Color.green())
            embed.add_field(name="Tekst:", value=message.clean_content)
            embed.set_image(url=message.attachments[0].url)
            await message.channel.send(embed=embed, view=view)
            return

        # Embed
        embed=disnake.Embed(title="Contact ADT&G beheer", description="Wil je dit versturen?", color=disnake.Color.green())
        await message.channel.send(embed=embed, view=view)


    # Making thread
    async def create_contact_with_staff(self, message):
        class Confirm(disnake.ui.View):

            def __init__(self):
                super().__init__(timeout=0)

            @disnake.ui.button(label="Afwijzen", style=disnake.ButtonStyle.grey)
            async def cancel(self_inside_button, button: disnake.ui.Button, inter: disnake.MessageInteraction):
                msg = await inter.response.send_message("Ik heb het verzoek afgewezen!")
                thread_to_close= self.bot.get_channel(inter.channel.id)
                name_thread = thread_to_close.name
                
                await thread_to_close.edit(name=f"(gesloten){name_thread}", locked=True, archived=True)
                await modmail.accept_or_deny(self, message, type=False, by_user=inter.author.name)

        view = Confirm()

        # Get admin and mod roles
        guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
        role_admin = guild.get_role(Role_ids.ADMIN)
        role_moderator = guild.get_role(Role_ids.MODERATOR)

        channel = self.bot.get_channel(env_variable.MODMAIL_ID)
        thread  = await channel.create_thread(name=f"{str(message.author.name)}&&MM", reason=f"ModMail for {message.author.name}", type=None, message=msg)
        
        class Deny(disnake.ui.View):

            def __init__(self):
                super().__init__(timeout=0)

            @disnake.ui.button(label="Afwijzen", style=disnake.ButtonStyle.grey)
            async def cancel(self_inside_button, button: disnake.ui.Button, inter: disnake.MessageInteraction):
                msg = await inter.response.send_message("Ik heb het verzoek afgewezen!")
                thread_to_close= self.bot.get_channel(inter.channel.id)
                name_thread = thread_to_close.name
                
                await thread_to_close.edit(name=f"(gesloten){name_thread}", locked=True, archived=True)
                await modmail.accept_or_deny(self, message, type=False, by_user=inter.author.name)

        view = Deny()

        # If message is an image
        if message.attachments:
            embed=disnake.Embed(title="Nieuwe ticket", description=f"Van user: {message.author.name}", color=disnake.Color.red())
            embed.add_field(name="Tekst:", value=message.clean_content)
            embed.set_image(url=message.attachments[0].url)
            await thread.send(embed=embed, view=Deny)
            return

        # Embed 
        embed=disnake.Embed(title="Nieuwe ticket", description=f"Van user: {message.author.name}", color=disnake.Color.red())
        embed.add_field(name=f"Vraag:", value=str(message.clean_content), inline=True)
        await thread.send(embed=embed, view=Deny)

        
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
        embed.add_field(name=f"Info:", value="Als je vraag niet beantwoord is, dan kun je hieronder gewoon terugtypen! (In 1 bericht)", inline=False)

        await member.send(embed=embed)



    # Closing thread
    async def close_ticket_and_thread(self, message, member):
        class Confirm(disnake.ui.View):

            def __init__(self):
                super().__init__(timeout=0)            

            @disnake.ui.button(label="Sluit ticket", style=disnake.ButtonStyle.red)
            async def confirm(self_inside_button, button: disnake.ui.Button, inter: disnake.MessageInteraction):
                
                await inter.response.send_message("Ik heb de ticket gesloten!")
                embed=disnake.Embed(title="Contact ADT&G ticket gesloten!", description=f"Door: `{message.author.name}`", color=disnake.Color.red())
                await member.send(embed=embed)
                self_inside_button.stop()

                thread_to_close= self.bot.get_channel(message.channel.id)
                name_thread = thread_to_close.name
                await thread_to_close.edit(name=f"(gesloten){name_thread}", locked=True, archived=True)
                self_inside_button.stop()

        view = Confirm()        

        if message.attachments:
            embed=disnake.Embed(title="Je hebt dit gestuurd:", description=str(message.clean_content), color=disnake.Color.green())
            embed.set_image(url=message.attachments[0].url)
            await message.channel.send(embed=embed, view=view)
            await message.delete()
            return
        
        embed=disnake.Embed(title="Je hebt dit gestuurd:", description=str(message.clean_content), color=disnake.Color.green())
        await message.channel.send(embed=embed, view=view)
        await message.delete()


    async def send_user_response(self, message, thread_to_send):
        class Confirm(disnake.ui.View):

            def __init__(self):
                super().__init__(timeout=0)
                
            @disnake.ui.button(label="Sluit ticket", style=disnake.ButtonStyle.red)
            async def confirm(self_inside_button, button: disnake.ui.Button, inter: disnake.MessageInteraction):
                
                await inter.response.send_message("Ik heb de ticket gesloten!")
                embed=disnake.Embed(title="Contact ADT&G ticket gesloten!", description=f"Door: `{inter.author.name}`", color=disnake.Color.red())
                await message.author.send(embed=embed)
                self_inside_button.stop()

                thread_to_close= self.bot.get_channel(inter.channel.id)
                name_thread = thread_to_close.name
                await thread_to_close.edit(name=f"(gesloten){name_thread}", locked=True, archived=True)
                self_inside_button.stop()

        view = Confirm()  

        if message.attachments:
            embed=disnake.Embed(title="User reageerde met de afbeelding:", description=str(message.clean_content), color=disnake.Color.red())
            embed.set_image(url=message.attachments[0].url)            
            await thread_to_send.send(embed=embed, view=view)
            return

        embed=disnake.Embed(title="User reageerde:", description=str(message.clean_content), color=disnake.Color.red())
        await thread_to_send.send(embed=embed, view=view)


    # Log modmail actions to LOG channel
    async def logging(self, from_user, interaction, on_user):
        print(from_user, interaction, on_user)


def setup(bot: commands.Bot):
    bot.add_cog(modmail(bot))