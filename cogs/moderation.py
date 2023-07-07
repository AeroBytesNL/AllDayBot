import disnake
from disnake.ext import commands
from env import *
from helpers.command_restriction import *


# TODO: Make unban system
# Make user notification system

class moderation(commands.Cog):



    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Moderation is loaded!")
        


    # Commands 
    @commands.default_member_permissions(moderate_members=True)
    @commands.slash_command()
    async def moderatie(self, inter):
        pass



    # Get action menu
    @moderatie.sub_command(description = "Voer een moderatie actie uit")
    async def actie(self, inter, gebruiker: disnake.Member, reden:str):
        try:
            await moderation.embed_controller(self, inter, user=gebruiker, reason=reden)

        except Exception as error:
            await inter.response.send_message(str(error), ephemeral=True)



    # Get menu list
    @moderatie.sub_command(description = "Krijg van een gebruiker alle moderatie acties te zien")
    async def lijst(self, inter, gebruiker: disnake.Member = None, gebruiker_id = None):
        try:

            if gebruiker == None and gebruiker_id == None:
                await inter.response.send_message("Je moet een gebruiker invullen bij de optionele opties!", ephemeral=True)
                return                 

            if gebruiker != None:
                data = moderation.get_warning_info_by_user_id(user_id=gebruiker.id)
            else:
                data = moderation.get_warning_info_by_user_id(user_id=gebruiker_id)
            
            await moderation.user_info_embed(inter, data)

        except Exception as error:
            await inter.response.send_message(str(error), ephemeral=True)



    # Delete entry
    @moderatie.sub_command(description = "Verwijder een moderatie actie uit de log")
    async def verwijder(self, inter, entry_id):

            moderation.delete_entry(entry_id)
            await inter.response.send_message(f"Klaar! Entry {entry_id} is deleted!", ephemeral=True)



    # Manual add entry
    @moderatie.sub_command(description = "Voeg handmatig een entry toe aan de log")
    async def toevoegen(self, inter, reden:str, actie_uitgevoerd: str, gebruiker: disnake.Member = None, gebruiker_id = None):
        try:

            if gebruiker == None and gebruiker_id == None:
                await inter.response.send_message("Je moet een gebruiker invullen bij de optionele opties!", ephemeral=True)
                return 
            
            if gebruiker != None:
                moderation.insert_entry_manual(user=gebruiker.id, inter=inter, reason=reden, action=actie_uitgevoerd)
            else:
                moderation.insert_entry_manual(user=gebruiker_id, inter=inter, reason=reden, action=actie_uitgevoerd)

            await inter.response.send_message("De log is toegevoegd!")

        except Exception as error:
            await inter.response.send_message(str(error), ephemeral=True)



    # Main controller
    async def embed_controller(self, inter, user, reason):

        # Get data from user in warning system
        user_data = moderation.get_warning_info_by_user_id(user_id=user.id)

        # Send first embed with data
        await moderation.action_embed(self, inter, user, reason, user_data)



    # Second controller
    async def punishment_execution_controller(self, inter, callback_reaction, user, user_data, reason):

        # Get guild object
        guild = self.bot.get_guild(env_variable.GUILD_ID)

        # Execute punishment
        # Mute
        if callback_reaction == "Mute 30 minuten":
            # Send notification to end yser
            await moderation.user_notification_embed_dm(self, user_id=user.id, admin=inter.author.name, punishment=callback_reaction, reason=reason)
            await guild.timeout(disnake.Object(user.id), duration=1800)
            # Insert action into DB
            moderation.insert_action(user_id=user.id, action="Mute 30 minuten", inter=inter, violation=reason)
        elif callback_reaction == "Mute 1 uur":
            await moderation.user_notification_embed_dm(self, user_id=user.id, admin=inter.author.name, punishment=callback_reaction, reason=reason)
            await guild.timeout(disnake.Object(user.id), duration=3600)
            moderation.insert_action(user_id=user.id, action="Mute 1 uur", inter=inter, violation=reason)
        elif callback_reaction == "Mute 12 uur":
            await moderation.user_notification_embed_dm(self, user_id=user.id, admin=inter.author.name, punishment=callback_reaction, reason=reason)
            await guild.timeout(disnake.Object(user.id), duration=43200)
            moderation.insert_action(user_id=user.id, action="Mute 12 uur", inter=inter, violation=reason)
        elif callback_reaction == "Mute 24 uur":
            await moderation.user_notification_embed_dm(self, user_id=user.id, admin=inter.author.name, punishment=callback_reaction, reason=reason)
            await guild.timeout(disnake.Object(user.id), duration=86400)
            moderation.insert_action(user_id=user.id, action="Mute 24 uur", inter=inter, violation=reason)            

        # Ban
        elif callback_reaction == "Ban voor 1 dag":
            await moderation.user_notification_embed_dm(self, user_id=user.id, admin=inter.author.name, punishment=callback_reaction, reason=reason)
            await guild.ban(user=user, reason=reason, clean_history_duration=0)
            moderation.insert_action(user_id=user.id, action="Ban 1 dag", inter=inter, violation=reason)
        elif callback_reaction == "Ban voor 1 week":
            await moderation.user_notification_embed_dm(self, user_id=user.id, admin=inter.author.name, punishment=callback_reaction, reason=reason)
            await guild.ban(user=user, reason=reason, clean_history_duration=0)
            moderation.insert_action(user_id=user.id, action="Ban 1 week", inter=inter, violation=reason)
        elif callback_reaction == "Ban voor altijd":
            await moderation.user_notification_embed_dm(self, user_id=user.id, admin=inter.author.name, punishment=callback_reaction, reason=reason)
            await guild.ban(user=user, reason=reason, clean_history_duration=0)
            moderation.insert_action(user_id=user.id, action="Ban altijd", inter=inter, violation=reason)



    # Main functions
    async def action_embed(self, inter, user, reason, user_data):
        
        second_self = self
        
        # Embed with user info
        embed=disnake.Embed(title="Gebruiker actie informatie", description=f"Aantal acties: {len(user_data)}", color=0xdf8cfe)
        
        for action in user_data: 
            embed.add_field(name=f"Admin: {action[1]} **-** ID: {action[4]}", value=f"Actie: {action[2]} **-** Reden: {action[3]}", inline=False)

        # Select menu
        class Dropdown(disnake.ui.StringSelect):
            def __init__(self):
                # Define the options that will be presented inside the dropdown
                options = [

                    disnake.SelectOption(
                        label="Mute 30 minuten", description="Mute iemand voor 30 minuten", emoji="🔊"
                    ),
                    disnake.SelectOption(
                        label="Mute 1 uur", description="Mute iemand voor 1 uur", emoji="🔊"
                    ),
                    disnake.SelectOption(
                        label="Mute 12 uur", description="Mute iemand voor 12 uur", emoji="🔊"
                    ),
                    disnake.SelectOption(
                        label="Mute 24 uur", description="Mute iemand voor 24 uur", emoji="🔊"
                    ),
                    disnake.SelectOption(
                        label="Ban voor 1 dag", description="Ban iemand voor 1 dag", emoji="❗"
                    ),
                    disnake.SelectOption(
                        label="Ban voor 1 week", description="Ban iemand voor 1 week", emoji="❗"
                    ),
                    disnake.SelectOption(
                        label="Ban voor altijd", description="Ban iemand voor altijd", emoji="❗"
                    )                                                                                                                                         
                ]

                super().__init__(
                    placeholder="Voer een actie uit op de overstreder",
                    min_values=1,
                    max_values=1,
                    options=options,
                )

            # Callback
            async def callback(self, inter: disnake.MessageInteraction):
                await inter.response.send_message(f"Je hebt {self.values[0]} gekozen!", ephemeral=True)
                callback_reaction = self.values[0]
                await moderation.punishment_execution_controller(second_self, inter, callback_reaction, user, user_data, reason)

        class DropdownView(disnake.ui.View):

            def __init__(self):
                super().__init__()

                # Add the dropdown to our view object.
                self.add_item(Dropdown())

        view = DropdownView()

        await inter.response.send_message(embed=embed,view=view, ephemeral=True)



    async def user_info_embed(inter, data):

        # Embed with user info
        embed=disnake.Embed(title="Gebruiker actie informatie", description=f"Aantal acties: **{len(data)}**", color=0xdf8cfe)
        
        for action in data: 
            embed.add_field(name=f"Admin: {action[1]} **-** ID: {action[4]}", value=f"**Actie:** {action[2]} **Reden:** {action[3]} **Tijd:** {action[5]}", inline=False)

        await inter.response.send_message(embed=embed, ephemeral=True)



    async def user_notification_embed_dm(self, user_id, admin, punishment, reason):

        # Getting user
        user = await self.bot.get_or_fetch_user(user_id)

        embed=disnake.Embed(title="Moderatie actie van ADT&G", description=f"Door admin: {admin}", color=0xdf8cfe)
        embed.add_field(name=f"Actie uitgevoerd:", value=str(punishment), inline=False)
        embed.add_field(name=f"Reden:", value=str(reason), inline=False)
        if "Mute" in punishment:
            embed.add_field(name=f"Niet eens met deze actie?", value="Vul het formulier in op: https://alldaytechandgaming.nl/moderatie-actie-aanvechten-2/ of stuur onze bot een DM.", inline=False)
        else:
            embed.add_field(name=f"Niet eens met deze actie?", value="Vul het formulier in op: https://alldaytechandgaming.nl/moderatie-actie-aanvechten-2/", inline=False)

        await user.send(embed=embed)



    # Database querys
    def get_warning_info_by_user_id(user_id):
        Database.cursor.execute(f"SELECT * FROM warning_system WHERE user_id = {user_id}")
        return Database.cursor.fetchall()
    


    def insert_action(user_id, action, inter, violation):
        Database.cursor.execute(f"INSERT INTO warning_system (user_id, warning_maker, action, violation) VALUES ({user_id}, '{inter.author.name}', '{action}', '{violation}')")
        Database.db.commit()



    def delete_entry(entry_id):
        Database.cursor.execute(f"DELETE FROM warning_system WHERE entry_id = {entry_id}")
        Database.db.commit()



    def insert_entry_manual(user, inter, reason, action):
        Database.cursor.execute(f"INSERT INTO warning_system (user_id, warning_maker, action, violation) VALUES ({user}, '{inter.author.name}', '{action}', '{reason}')")
        Database.db.commit()




def setup(bot: commands.Bot):
    bot.add_cog(moderation(bot))