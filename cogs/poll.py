import disnake 
from disnake.ext import commands
from env import *


class Poll(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.ongoing_polls = {}


    # ADT&G poll functie
    @commands.slash_command()
    async def poll_aanmaken(self, inter, poll_vraag, vraag_1, vraag_2, vraag_3 = None, vraag_4 = None
    , vraag_5 = None, vraag_6 = None, vraag_7 = None, vraag_8 = None, vraag_9 = None, vraag_10 = None
    , vraag_11 = None, vraag_12 = None, vraag_13 = None, vraag_14 = None, vraag_15 = None):       
        embed = await Poll.poll(self, inter, poll_vraag, vraag_1, vraag_2, vraag_3, vraag_4, vraag_5, vraag_6
            , vraag_7, vraag_8, vraag_9, vraag_10, vraag_11, vraag_12, vraag_13, vraag_14, vraag_15)

        msg_sended = await inter.response.send_message(embed=embed)
        msg = await inter.original_message()

        self.ongoing_polls.update({msg.id: {"🇦", "🇧"}})

        await msg.add_reaction("🇦")
        await msg.add_reaction("🇧")
        
        if vraag_3 != None:
            await msg.add_reaction("🇨")
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨"}})
        if vraag_4 != None:
            await msg.add_reaction("🇩")
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨"}})
        if vraag_5 != None:
            await msg.add_reaction("🇪")
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨", "🇪"}})
        if vraag_6 != None:
            await msg.add_reaction("🇫")
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨", "🇪", "🇫"}})
        if vraag_7 != None:
            await msg.add_reaction("🇬")
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨", "🇪", "🇫", "🇬"}})
        if vraag_8 != None:
            await msg.add_reaction("🇭")      
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨", "🇪", "🇫", "🇬", "🇭"}})
        if vraag_9 != None:
            await msg.add_reaction("🇮")
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨", "🇪", "🇫", "🇬", "🇭", "🇮"}})
        if vraag_10 != None:
            await msg.add_reaction("🇯")
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯"}})
        if vraag_11 != None:
            await msg.add_reaction("🇰")            
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰"}})
        if vraag_12 != None:
            await msg.add_reaction("🇱")
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱"}})
        if vraag_13 != None:
            await msg.add_reaction("🇲")
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲"}})
        if vraag_14 != None:
            await msg.add_reaction("🇴")       
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇴"}})
        if vraag_15 != None:
            await msg.add_reaction("🇵")                 
            self.ongoing_polls.update({msg.id: {"🇦", "🇧", "🇨", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇴", "🇵"}})
        
        await Poll.log_command(self, author=inter.author, command="`/poll_aanmaken`", channel=inter.channel)


    # Creating a poll, 15 options
    async def poll(self, inter, poll_vraag, vraag_1, vraag_2, vraag_3, vraag_4, vraag_5, vraag_6
        , vraag_7, vraag_8, vraag_9, vraag_10, vraag_11, vraag_12, vraag_13, vraag_14, vraag_15):

        embed=disnake.Embed(title="Poll", description=f"**{poll_vraag}**", color=0xdf8cfe)
        embed.add_field(name=f"🇦 - {vraag_1}", value="\u200b", inline=False)
        embed.add_field(name=f"🇧 - {vraag_2}", value="\u200b", inline=False)
        
        if vraag_3 != None:
            embed.add_field(name=f"🇨 - {vraag_3}", value="\u200b", inline=False)
        if vraag_4 != None:
            embed.add_field(name=f"🇩 - {vraag_4}", value="\u200b", inline=False)
        if vraag_5 != None:
            embed.add_field(name=f"🇪 - {vraag_5}", value="\u200b", inline=False)        
        if vraag_6 != None:
            embed.add_field(name=f"🇫 - {vraag_6}", value="\u200b", inline=False)        
        if vraag_7 != None:
            embed.add_field(name=f"🇬 - {vraag_7}", value="\u200b", inline=False)        
        if vraag_8 != None:
            embed.add_field(name=f"🇭  - {vraag_8}", value="\u200b", inline=False)
        if vraag_9 != None:
            embed.add_field(name=f"🇮 - {vraag_9}", value="\u200b", inline=False)
        if vraag_10 != None:
            embed.add_field(name=f"🇯 - {vraag_10}", value="\u200b", inline=False)         
        if vraag_11 != None:
            embed.add_field(name=f"🇰 - {vraag_11}", value="\u200b", inline=False)        
        if vraag_12 != None:
            embed.add_field(name=f"🇱 - {vraag_12}", value="\u200b", inline=False)        
        if vraag_13 != None:
            embed.add_field(name=f"🇲 - {vraag_13}", value="\u200b", inline=False)        
        if vraag_14 != None:
            embed.add_field(name=f"🇴 - {vraag_14}", value="\u200b", inline=False)        
        if vraag_15 != None:
            embed.add_field(name=f"p - {vraag_15}", value="\u200b", inline=False)   

        guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
        embed.set_thumbnail(url=guild.icon)

        embed.set_footer(text=f"Deze poll is gemaakt door {inter.author.name}")

        return embed


    # Command logging
    async def log_command(self, author, command, channel):

        embed=disnake.Embed(title=f"Een user heeft een command gebruikt!", description=f"\n", color=disnake.Color.green())
        embed.add_field(name="Command::", value=str(command), inline=True)
        embed.add_field(name="Author:", value=str(author.mention), inline=True)
        embed.add_field(name="Kanaal:", value=str(channel.mention), inline=False)
        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        await channel_to_send.send(embed=embed)


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        try:
            if user.id == self.bot.user.id: return

            if reaction.message.id not in self.ongoing_polls: return 

            if reaction.emoji not in self.ongoing_polls[reaction.message.id]:
                await reaction.clear()
                await Poll.log_added_reactions_poll(self, reaction, user)
        except Exception as error:
            print(error)
            pass


    async def log_added_reactions_poll(self, reaction, user):
        embed=disnake.Embed(title=f"Een user wou een reactie op een poll doen die niet in de poll zat!", description=f"\n", color=disnake.Color.green())
        embed.add_field(name="Gebruiker:", value=user.mention, inline=True)
        embed.add_field(name="Reactie:", value=reaction.emoji, inline=True)
        channel_to_send = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        await channel_to_send.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Poll(bot))