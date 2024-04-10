import disnake
from disnake.ext import commands
from env import *
import time


class Introduce_remover(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Introduce remover is loaded!")
        

    # Deletes introduction if there already is an introduction of that member
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return

        # Do nothing if message wasn't send in introduction channel
        if message.channel.id != Channel.STEL_JEZELF_VOOR:
            return

        channel = self.bot.get_channel(Channel.STEL_JEZELF_VOOR)
        excisting_introductions = await channel.history(limit=1000).flatten() 

        counter = 0
        for introduction in excisting_introductions:
            if introduction.author.id == message.author.id:
                counter +=1

        if counter <= 1:
            counter = 0
            return        
        
        await message.delete()
        print("Message deleted from user that wanted to post a second time in introduction")
        msg = await channel.send("Je bericht is verwijderd, maximaal één bericht is toegestaan!")
        time.sleep(5)
        await msg.delete()
        counter = 0


    # Deletes an introduction if an member leaves
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(Channel.STEL_JEZELF_VOOR)
        messages_in_channel = await channel.history(limit=1000).flatten()

        for message in messages_in_channel:
            if message.author.id != member.id:
                return
            print(f"#stel-jezelf-voor message deleted from user {member.display_name}")
            await message.delete()
            await Introduce_remover.log_removed_introduction(self, member)


    async def log_removed_introduction(self, member):
        channel = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        embed=disnake.Embed(title="#stel-jezelf-voor bericht automatisch verwijderd van:", description=f"{member.display_name}", color=disnake.Color.red())
        await channel.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Introduce_remover(bot))