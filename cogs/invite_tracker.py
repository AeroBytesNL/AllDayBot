import disnake
from disnake.ext import commands, tasks
from env import *
from helpers.error import Log
from datetime import datetime
from dateutil import relativedelta
from database import Database

class InviteTracker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Loaded Cog Invite tracker")
        self.invites = []

    @commands.Cog.listener()
    async def on_ready(self):
        self.invites = await self.bot.get_guild(env_variable.GUILD_ID).invites()

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        self.invites = await self.bot.get_guild(env_variable.GUILD_ID).invites()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        for old_invite in self.invites:
            for current_invite in await self.bot.get_guild(env_variable.GUILD_ID).invites():
                if old_invite.code == current_invite.code and old_invite.uses < current_invite.uses:
                    await InviteTracker.member_guild_embed(self, member, "joinde de keet!", current_invite.code, current_invite.inviter)

    @commands.default_member_permissions(moderate_members=True)
    @commands.slash_command(description="Voeg een nieuwe invite beschrijving toe")
    async def invite_toevoegen(self, inter, uitnodigingscode: str, invite_beschrijving: str):
        try:
            Database.cursor.execute(f"INSERT INTO invite_tracker (code, description) VALUES ('{uitnodigingscode}', '{invite_beschrijving}')")
            Database.db.commit()
        except Exception as error:
            Log.error(f"Error inside \"invite_toevoegen\": {error}")
            await inter.response.send_message("Er ging iets mis!")
            return

        await inter.response.send_message("Invite beschrijving is toegevoegd!", ephemeral=True)

    @commands.default_member_permissions(moderate_members=True)
    @commands.slash_command(description="Krijg een lijst te zien van invite beschrijvingen")
    async def invite_lijst(self, inter):
        try:
            Database.cursor.execute("SELECT * FROM invite_tracker")
            res = Database.cursor.fetchall()

            embed = disnake.Embed(title="Invite beschrijvingen!")
            for invite_description in res:
                embed.add_field(name=f"ID: {invite_description[0]} - Code: {invite_description[1]}", value=invite_description[2])
        except Exception as error:
            Log.error(f"Error inside \"invite_lijst\": {error}")
            await inter.response.send_message("Er ging iets mis!")
            return

        await inter.response.send_message(embed=embed, ephemeral=True)

    @commands.default_member_permissions(moderate_members=True)
    @commands.slash_command(description="Verwijder een invite beschrijving")
    async def invite_verwijder(self, inter, invite_id: int):
        try:
            Database.cursor.execute(f"DELETE FROM invite_tracker WHERE id = {invite_id}")
            Database.db.commit()
        except Exception as error:
            Log.error(f"Error inside \"invite_verwijder\": {error}")
            await inter.response.send_message("Er ging iets mis!")
            return

        await inter.response.send_message("Invite beschrijving is verwijderd!", ephemeral=True)

    async def member_guild_embed(self, member, join_type, invite_code, inviter):
        try:
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
            match join_type:
                case "joinde de keet!":
                    embed_color = disnake.Color.green()
                case "verliet de keet!":
                    embed_color = disnake.Color.dark_red()
                case "is verbannen van deze keet!":
                    embed_color = disnake.Color.dark_red()
                case "is un-banned van deze keet!":
                    embed_color = disnake.Color.dark_red()

            embed = disnake.Embed(title="\n", description=f"**{member.mention} {join_type}**",
                                  color=embed_color)
            embed.set_author(name=member.display_name, icon_url=member.avatar)
            embed.add_field(name="Account leeftijd:", value=str(i), inline=False)
            embed.add_field(name="Invite code:", value=str(invite_code), inline=False)
            embed.add_field(name="Invite author:", value=str(inviter.name), inline=False)

            channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await channel_to_send.send(embed=embed)
        except Exception as error:
            Log.error(f"Error while executing \"member_guild_embed\": {error}")

def setup(bot: commands.Bot):
    bot.add_cog(InviteTracker(bot))
