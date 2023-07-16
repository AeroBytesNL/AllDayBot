import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database


class analytics(commands.Cog):



    def __init__(self, bot: commands.Bot):

        self.bot = bot
        print("Cog Analytics is loaded!")

        # Starting loopies
        self.member_statistics.start()
        self.save_general_statistics_to_db.start()

        # Storage global
        self.msg_storage = []
        self.total_members = 0
        self.members_online = 0



    # message statistics
    @commands.Cog.listener()
    async def on_message(self, message):
        
        # Do nothing if message if from bot
        if message.author == self.bot.user:
            return
        
        # Adding message with channel to storage
        self.msg_storage.append(str(message.channel))



    # Updating total members
    @tasks.loop(seconds=5)
    async def member_statistics(self):
        
        # Getting guild
        guild = await self.bot.fetch_guild(env_variable.GUILD_ID)

        # Getting total members and add to storage
        self.total_members = int(guild.approximate_member_count)

        # Getting total online members and save it to storage
        self.members_online = int(guild.approximate_presence_count)

    

    # Saving stuff from self.storage to DB
    @tasks.loop(seconds=60)
    async def save_general_statistics_to_db(self):

        print("Saving new total analytics....")

        # Get current analytics
        Database.cursor.execute("SELECT * FROM statistics LIMIT 1")
        res = Database.cursor.fetchone()

        # Assign vars to statistics
        total_messages = len(self.msg_storage)

        # Most populair channels statistics
        textchannel_general = self.msg_storage.count("general")
        textchannel_memes = self.msg_storage.count("memes")
        textchannel_nsfw = self.msg_storage.count("nsfw")
        textchannel_tech_talk = self.msg_storage.count("tech-talk")
        textchannel_development_coding = self.msg_storage.count("development-coding")
        textchannel_games_talk = self.msg_storage.count("games-talk")
        textchannel_looking_for_party = self.msg_storage.count("looking-for-party")
        textchannel_games_media = self.msg_storage.count("games-media")

        # Update analytics 
        Database.cursor.execute(f"""UPDATE statistics SET total_members={self.total_members}, total_members_online={self.members_online}, 
        total_messages={int(res[2]) + total_messages}, textchannel_general={int(res[3]) + textchannel_general}, textchannel_memes={int(res[4]) + textchannel_memes},
        textchannel_nsfw={int(res[5]) + textchannel_nsfw}, textchannel_tech_talk={int(res[6]) + textchannel_tech_talk},
        textchannel_development_coding={int(res[7]) + textchannel_development_coding}, textchannel_games_talk={int(res[8]) + textchannel_games_talk},
        textchannel_looking_for_party={int(res[9]) + textchannel_looking_for_party}, textchannel_games_media={int(res[10]) + textchannel_games_media}
        """)
        Database.db.commit()

        # Clear storage
        self.msg_storage.clear()


    
def setup(bot: commands.Bot):
    bot.add_cog(analytics(bot))