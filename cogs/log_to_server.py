import disnake
from disnake.ext import commands, tasks
from disnake.enums import ButtonStyle
from env import *
from database import *
from datetime import datetime, date
from dateutil import relativedelta
import requests
import os
# @todo fix image remove logging


class log_to_server(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Log to server is loaded!")
        log_to_server.image_cache_cleaner.start(self)


    # Image cacher
    @commands.Cog.listener()
    async def on_message(self, message):
        # Do nothing if no atachments are precent
        if len(message.attachments) == 0:
            return
        
        attachment = message.attachments[0]

        # If filename doesn't end with those below then return
        if not attachment.filename.endswith(
            (
                ".png",
                ".jpg",
                ".jpeg",
                ".gif",
                ".webp"
            )):
            return

        # Save file, with a custom name
        img = requests.get(attachment.url).content
        with open(f"./files/alldaylog_image_cache/{message.id}.png", mode="wb") as file:
            file.write(img)
            file.close()
            print("Saved image file to cache")


    # Delete unused images from image cache older then 14 days
    @tasks.loop(seconds=60)
    async def image_cache_cleaner(self):
        print("Cleaning image cache")
        images = [f for f in os.listdir("./files/alldaylog_image_cache")]

        for image in images:
            image_time = os.path.getmtime(f"./files/alldaylog_image_cache/{image}")
            date_stamp = datetime.fromtimestamp(image_time)
            delta = datetime.now() - date_stamp
            
            if delta.days >= 7:
                os.remove(f"./files/alldaylog_image_cache/{image}")
                print(f"Deleted image from image cache")


    # Member guild
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if log_to_server.get_settings(setting="sw_join_leave"):
            print("Welcome! ", member)
            await self.member_guild_embed(member, type="joinde de keet!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if log_to_server.get_settings(setting="sw_join_leave"):
            print("Aaaah! er is een member/memberina weg!")
            await self.member_guild_embed(member, type="verliet de keet!")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        if log_to_server.get_settings(setting="sw_ban_unban"):
            print(f"Aaaah! User: {member} is gebanned van guild: {guild}.")
            await self.member_guild_embed(member, type="is verbannen van deze keet!")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        if log_to_server.get_settings(setting="sw_ban_unban"):
            print(f"Aaaah! User: {member} is ungebanned van guild: {guild}.")
            await self.member_guild_embed(member, type="is un-banned van deze keet!")    

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Nickname change log
        if log_to_server.get_settings(setting="sw_nickname_change"):
            if before.nick != after.nick:
                name_before = before.nick
                name_after = after.nick
                if name_after == None:
                    name_after = after.display_name
                await self.user_name_change(name_before, name_after)


    # Voice 
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if log_to_server.get_settings(setting="sw_vc_join_leave"):
            # member joins voice
            if before.channel is None and after.channel is not None: 
                await self.log_voice_state(member, vc_channel=after.channel, type="Joinde")
            # Member leaves voice
            elif after.channel is None and before.channel is not None:
                await self.log_voice_state(member, vc_channel=before.channel, type="Verliet")

            elif log_to_server.get_settings(setting="sw_vc_change"):
                # Member switches voice channels
                if before.channel != after.channel:
                    await self.log_voice_state(member, vc_channel=after.channel, type="Veranderde")
                

    # Messages in guild
    @commands.Cog.listener()
    async def on_message_delete(self, payload):
        if log_to_server.get_settings(setting="sw_message_deleted"):
            await self.message_deleted(payload, message=payload.content, channel=payload.channel)
            
    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, messages):
        if log_to_server.get_settings(setting="sw_message_deleted"):
            bulk_deleted_count = len(messages.message_ids)
            bulk_deleted_channel = messages.channel_id
            await self.message_bulk_deleted(count=bulk_deleted_count, channel=bulk_deleted_channel)
            
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if log_to_server.get_settings(setting="sw_message_edited"):
            channel = after.channel.mention
            author = before.author
            if before.clean_content != after.clean_content:
                before_content = before.clean_content
                after_content = after.clean_content
                jump_to_msg = after.jump_url
                await self.message_edited(before_content, after_content, channel, author, jump_to_msg)


    # Changes in guild and roles
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        await self.new_or_deleted_role(self, role, type="aangemaakt")
    
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        await self.new_or_deleted_role(self, role, type="verwijderd")

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if before.name != after.name:
            await self.edited_role(self, before, after)

        elif before.color != after.color:
            await self.color_change_role(self, before, after)


    # Channels
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await log_to_server.channel_change(self, channel, type="Nieuw kanaal")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        await log_to_server.channel_change(self, channel, type="Kanaal verwijderd")

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.name != after.name:
            await log_to_server.channel_name_change(self, before=before.name, after=after.name)


    # Audit
    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry):

        # If user deletes a message
        if "message_delete" in str(entry.action):
            embed=disnake.Embed(title=f"\n", description=f"Bericht verwijderd", color=disnake.Color.red())
            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            embed.add_field(name="Door admin:", value=str(entry.user), inline=True)
            embed.add_field(name="Bericht was van:", value=str(entry.target), inline=True)
            await channel_to_send.send(embed=embed)


    
    # Emoji 
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        print(set(before).symmetric_difference(set(after)))



    # Reaction emojis
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        # Do nothing if user is bot
        if payload.member == self.bot.user: return

        if log_to_server.get_settings(setting="sw_message_reaction"):
            print("Reactie toegevoegd", payload.emoji, payload.message_id, payload.user_id)
            await log_to_server.log_reactions(self, payload, type_embed="toegevoegd")


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if log_to_server.get_settings(setting="sw_message_reaction"):
            print("Reactie verwijderd", payload.emoji, payload.message_id, payload.user_id)
            await log_to_server.log_reactions(self, payload, type_embed="verwijderd")


    # Threads
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if log_to_server.get_settings(setting="sw_threads"):            
            await log_to_server.log_threads(self, thread, type_embed="aangemaakt")

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        if log_to_server.get_settings(setting="sw_threads"):            
            await log_to_server.log_threads(self, thread, type_embed="verwijderd")




    #
    # Functions
    #
    async def member_guild_embed(self, member, type):

        date_created_at = str(member.created_at).split(" ")[0]
        x = date_created_at.split("-")

        # get two dates
        d1 = f'{x[2]}/{x[1]}/{x[0]}'
        d2 = datetime.today().strftime('%d/%m/%Y')

        start_date = datetime.strptime(d1, "%d/%m/%Y")
        end_date = datetime.strptime(d2, "%d/%m/%Y")

        # Get the relativedelta between two dates
        delta = relativedelta.relativedelta(end_date, start_date)
        if str(delta.years) == "0":
            i = f"{delta.months} maanden en {delta.days} dagen"
        else:
            i = f"{delta.years} jaar,  {delta.months} maanden en {delta.days} dagen"

        # Color
        match type:
            case "joinde de keet!":
                embed_color = disnake.Color.green()
            case "verliet de keet!":
                embed_color = disnake.Color.dark_red()
            case "is verbannen van deze keet!":
                embed_color = disnake.Color.dark_red()
            case "is un-banned van deze keet!":
                embed_color = disnake.Color.dark_red()

        embed=disnake.Embed(title="\n", description=f"**{member.mention} {type}**", color=embed_color)
        embed.set_author(name=member.display_name, icon_url=member.avatar)
        embed.add_field(name="Account leeftijd:", value=str(i), inline=False)
        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        await channel_to_send.send(embed=embed)


    # Member username change
    async def user_name_change(self, name_before, name_after):

        embed=disnake.Embed(title=f"Server gebruikersnaam bewerkt", description=f"\n", color=disnake.Color.orange())
        embed.add_field(name="Voor het bewerken:", value=str(name_before), inline=False)
        embed.add_field(name="Na het bewerken:", value=str(name_after), inline=False)
        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        await channel_to_send.send(embed=embed)


    # Voice logging
    async def log_voice_state(self, member, vc_channel, type):
        match type:
            case "Joinde":
                embed_color = disnake.Color.green()
            case "Verliet":
                embed_color = disnake.Color.red()
            case "Veranderde":
                embed_color = disnake.Color.orange()

        embed=disnake.Embed(title=f"\n", description=f"**{member.mention} {type} voice kanaal: {vc_channel.mention}**", color=embed_color)
        embed.set_author(name=member.display_name, icon_url=member.avatar)
        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        await channel_to_send.send(embed=embed)


    # Message
    async def message_deleted(self, payload, message, channel):
        embed=disnake.Embed(title=f"\n", description=f"{payload.author.mention} verwijderde een bericht in {channel.mention}", color=disnake.Color.red())
        embed.set_author(name=payload.author.display_name, icon_url=payload.author.avatar)
        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)

        images = [f for f in os.listdir("./files/alldaylog_image_cache")]

        if str(f"{payload.id}.png") in images:
            with open(f"./files/alldaylog_image_cache/{payload.id}.png", mode="rb") as file:
                embed.add_field(name="Content:", value=str(payload.clean_content), inline=False)
                embed.add_field(name="Afbeelding:", value="Zie afbeelding hier beneden", inline=False)
                await channel_to_send.send(embed=embed)
                await channel_to_send.send(file=disnake.File(file))
                print("Sended file from cache to log channel")
        else:
            embed.add_field(name="Content:", value=str(payload.clean_content), inline=False)
            await channel_to_send.send(embed=embed)


    async def message_bulk_deleted(self, count, channel):

        channel_name = (await self.bot.fetch_channel(channel)).mention
        embed=disnake.Embed(title=f"\n", description=f"**Bulk berichten verwijderd in {channel_name} - Aantal: {count}**", color=disnake.Color.red())

        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        await channel_to_send.send(embed=embed)

    async def message_edited(self, before_content, after_content, channel, author, jump_to_msg):
        embed=disnake.Embed(title=f"\n", description=f"**Bericht bewerkt in {channel} - Door: {author.mention}**", color=disnake.Color.orange())
        embed.set_author(name=author.display_name, icon_url=author.avatar)
        embed.add_field(name="Voor het bewerken:", value=str(before_content), inline=False)
        embed.add_field(name="Na het bewerken:", value=str(after_content), inline=False)
        embed.add_field(name=f"Ga naar het bericht:", value=str(jump_to_msg), inline=False)

        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        await channel_to_send.send(embed=embed)





    # Roles
    async def new_or_deleted_role(self, role, type):
        match type:
            case "aangemaakt":
                embed_color = disnake.Color.green()
            case "verwijderd":
                embed_color = disnake.Color.red()
        embed=disnake.Embed(title=f"Rol {type}: {role}", description="\n", color=embed_color)

        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        await channel_to_send.send(embed=embed)
    
    async def edited_role(self, before, after):
        if str(before) != str(after):
            embed=disnake.Embed(title=f"Rol bewerkt", description="\n", color=disnake.Color.orange())
            embed.add_field(name="Voor het bewerken:", value=str(before), inline=False)
            embed.add_field(name="Na het bewerken:", value=str(after), inline=False)

            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await channel_to_send.send(embed=embed)
        else:
            pass

    async def color_change_role(self, before, after):
            embed=disnake.Embed(title=f"Rol {before.name} kleur bewerkt", description="\n", color=disnake.Color.orange())
            embed.add_field(name="Voor het bewerken:", value=str(before.color), inline=False)
            embed.add_field(name="Na het bewerken:", value=str(after.color), inline=False)

            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await channel_to_send.send(embed=embed)


    # Channels
    async def channel_change(self, channel, type):
            print(channel)
            match type:
                case "Nieuw kanaal":
                    embed_color = disnake.Color.green()
                case "Kanaal verwijderd":
                    embed_color = disnake.Color.green()

            embed=disnake.Embed(title=f"\n", description=f"**{type} met de naam: #{channel}**", color=embed_color)
            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await channel_to_send.send(embed=embed)   
                    
    async def channel_name_change(self, before, after):
            embed=disnake.Embed(title=f"Kanaal bewerkt", description="\n", color=disnake.Color.orange())
            embed.add_field(name="Voor het bewerken:", value=str(before), inline=False)
            embed.add_field(name="Na het bewerken:", value=str(after), inline=False)

            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await channel_to_send.send(embed=embed)            
    



    # Logging commands to log channel
    def log_commands(self, inter, command, on_user):
            embed=disnake.Embed(title=f"Adje log", description="\n", color=disnake.Color.dark_green())
            embed.set_author(name=inter.author.display_name, icon_url=inter.author.avatar)
            embed.add_field(name="Command:", value=str(command), inline=False)
            embed.add_field(name="Op gebruiker:", value=str(on_user), inline=False)

            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            self.bot.loop.create_task(channel_to_send.send(embed=embed))
            
    

    async def log_reactions(self, payload, type_embed):
            user = self.bot.get_user(payload.user_id)
            message = self.bot.get_message(payload.message_id)

            embed=disnake.Embed(title=f"Reactie {type_embed}", description="\n", color=disnake.Color.orange())
            embed.add_field(name=f"Emoji:", value=f"{payload.emoji}", inline=True)
            embed.add_field(name="Bericht:", value=f"{message.jump_url}", inline=True)
            embed.add_field(name="Door user:", value=f"{user.display_name}", inline=True)

            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await channel_to_send.send(embed=embed)            
    



    async def log_threads(self, thread, type_embed):
            print(f"Thread {type_embed}",thread.name, thread.category, thread.jump_url, thread.owner)


            embed=disnake.Embed(title=f"Thread {type_embed}", description="\n", color=disnake.Color.orange())
            embed.add_field(name=f"Threadnaam:", value=f"{thread.name}", inline=True)
            embed.add_field(name="In category:", value=f"{thread.category}", inline=True)
            embed.add_field(name="Van gebruiker:", value=f"{thread.owner}", inline=True)

            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await channel_to_send.send(embed=embed)            
    


    def get_settings(setting):

            Database.cursor.execute(f"SELECT {setting} FROM bot_settings LIMIT 1")
            res = Database.cursor.fetchone()[0]

            if res == 1:
                return True
            else:
                return False
         


def setup(bot: commands.Bot):
    bot.add_cog(log_to_server(bot))