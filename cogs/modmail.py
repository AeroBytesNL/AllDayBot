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

            if i == True:
                channel = self.bot.get_channel(1093873145984860222)
                message = await channel.send(f"Nieuwe ModMail ticket van {message.author.display_name}!")

                await channel.create_thread(
                    name="This thread requires a starting message to be specified.",
                    auto_archive_duration=60,
                    message=message
                )
                return

        # if message is in a thread from server to user
        if hasattr(message, "thread"):
            if not isinstance(message.channel, disnake.channel.DMChannel):
                if "MM" in str(message.channel.name):
                    username_to_send = str(message.channel.name).split("&&")[0]
                    for member in self.bot.get_all_members():
                        if member.name == username_to_send:
                            await modmail.send_admin_response_to_ticket_maker(self, message, member)
                            await modmail.close_ticket_and_thread(self, message, member)

def setup(bot: commands.Bot):
    bot.add_cog(modmail(bot))