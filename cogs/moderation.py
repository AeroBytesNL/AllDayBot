import disnake
from disnake.ext import commands
from env import *
from database import Database
from helpers.error import Log

# TODO: Make unban system
# Make user notification system

class moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Loaded Cog moderation")

    # Commands
    # Mother Off All Commands
    @commands.slash_command()
    async def mod(self, inter):
        pass

    # Logging kick/ban/timeout
    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry):
        # Kick 
        if entry.action == disnake.AuditLogAction.kick:
            await moderation.log_to_mod_log(self, action="Kick", reason=entry.reason, action_maker=entry.user.display_name, action_member=entry.target.display_name)
            moderation.save_moderation_action_to_db(action="Kick", reason=entry.reason, action_maker=entry.user, action_member=entry.target)
            # Save to database

        # Ban 
        elif entry.action == disnake.AuditLogAction.ban:
            await moderation.log_to_mod_log(self, action="Ban", reason=entry.reason, action_maker=entry.user.display_name, action_member=entry.target.display_name)
            moderation.save_moderation_action_to_db(action="Ban", reason=entry.reason, action_maker=entry.user, action_member=entry.target)

        # Added timeout
        elif entry.before.timeout == None and entry.after.timeout != None:
            await moderation.log_to_mod_log(self, action=f"Timeout toegevoegd tot {entry.after.timeout}", reason=entry.reason, action_maker=entry.user.display_name, action_member=entry.target.display_name)
            moderation.save_moderation_action_to_db(action=f"Timeout toegevoegd tot {entry.after.timeout}", reason=entry.reason, action_maker=entry.user, action_member=entry.target)

        # removed timeout
        elif entry.before.timeout != None and entry.after.timeout == None:
            await moderation.log_to_mod_log(self, action="Timeout verwijderd", reason=entry.reason, action_maker=entry.user.display_name, action_member=entry.target.display_name)
            moderation.save_moderation_action_to_db(action="Timeout verwijderd", reason=entry.reason, action_maker=entry.user, action_member=entry.target)

        # Make command that gets al the bad people and returns it by number and alphabetic order
        # Make command that then can get the user from the saved DB and return all information

    def save_moderation_action_to_db(action, reason, action_maker, action_member):
        Database.cursor.execute(
        f"INSERT INTO moderation_log (user_id, user_name, moderation_reason, moderation_action_taker, moderation_action) VALUES ({action_member.id}, '{action_member.display_name}', '{reason}', '{action_maker.display_name}', '{action}')")
        Database.db.commit()

    async def log_to_mod_log(self, action, reason, action_maker, action_member):
        channel = self.bot.get_channel(Channel.BLACKLISTMODLOG)

        embed=disnake.Embed(title=f"Er is een {action} uitgevoerd!", description=f"beheerder: {action_maker}", color=disnake.Color.red())
        embed.add_field(name=f"Lid: {action_member}", value=f"**Reden: {reason}**", inline=True)
        
        await channel.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(moderation(bot))