import disnake
from disnake.ext import commands, tasks
from env import *
import time
import random
from database import Database

class Quiz(commands.Cog):



    def __init__(self, bot: commands.Bot):

        self.bot = bot
        print("Cog Quiz is loaded!")
        self.ongoing_quizes_ids = []
        self.quiz_storage = {}



    # Listening to ongoing quized
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        # check if reaction is from bot, if it is return
        if user == self.bot.user:
            return
        
        # If quiz in storage
        if reaction.message.id in self.ongoing_quizes_ids:
            pass



    # Mother Of All Commands
    @commands.slash_command()
    async def quiz(self, inter):
        pass



    # Quiz make command
    @quiz.sub_command(description="Maak een quiz aan")
    async def aanmaken(self, inter, quiz_titel, quiz_vraag, juiste_antwoord, antwoord_1, antwoord_2, quiz_start_tijd:commands.option_enum({"Geen vertraging": 0, "5 seconden": 5, "10 seconden": 10, "15 seconden": 15, "20 seconden": 10, "30 seconden": 10, "45 seconden": 10, "1 minuut": 10, "2 minuten": 120, "3 minuten": 180}), quiz_sluit_tijd:int = 15, antwoord_3 = None, antwoord_4 = None):

        # Generate quiz ID
        quiz_id = random.randint(0, 10000)

        # Save to DB!

        if quiz_start_tijd != 0:
            await Quiz.quiz_first_embed(self, inter, quiz_titel, antwoord_1, antwoord_2, antwoord_3, antwoord_4, quiz_start_tijd, quiz_sluit_tijd, quiz_id)

            time.sleep(quiz_start_tijd)

        second_embed = await Quiz.quiz_second_embed(self, inter, quiz_titel, quiz_vraag, antwoord_1, antwoord_2, antwoord_3, antwoord_4, quiz_sluit_tijd, channel=inter.channel, quiz_id=quiz_id)

        # Saving quid id in ongoing quizes
        self.ongoing_quizes_ids.append(second_embed.message.id)

        time.sleep(quiz_sluit_tijd)



    # Quiz embed
    async def quiz_first_embed(self, inter, quiz_titel, antwoord_1, antwoord_2, antwoord_3, antwoord_4, quiz_start_tijd, quiz_sluit_tijd, quiz_id):

        embed=disnake.Embed(title="Quiz!", description=f"**{quiz_titel}**", color=0xdf8cfe)
        embed.add_field(name=f"Quiz begint", value=disnake.utils.format_dt(time.time() + quiz_start_tijd, 'R'), inline=False)
        embed.add_field(name=f"Quiz antwoord tijd", value=f"{quiz_sluit_tijd}s", inline=False)
        embed.add_field(name=f"Quiz is gemaakt door:", value=inter.author.mention, inline=False)

        embed.set_footer(text=f"Quiz ID: {quiz_id}")

        guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
        embed.set_thumbnail(url=guild.icon)

        msg = await inter.response.send_message(embed=embed)
        return msg



    async def quiz_second_embed(self, inter, quiz_titel, quiz_vraag, antwoord_1, antwoord_2, antwoord_3, antwoord_4, quiz_sluit_tijd, channel, quiz_id):

        embed=disnake.Embed(title=f"Quiz! - {quiz_titel}", description=f"**{quiz_vraag}**", color=0xdf8cfe)
        
        if antwoord_3 == None and antwoord_4 == None:
            embed.add_field(name="Antwoorden:", value=f"🇦 {antwoord_1}\n🇧 {antwoord_2}")

        elif antwoord_3 != None and antwoord_4 == None:
            embed.add_field(name="Antwoorden:", value=f"🇦 {antwoord_1}\n🇧 {antwoord_2}\n🇨 {antwoord_3}")
        
        elif antwoord_3 != None and antwoord_4 != None:
            embed.add_field(name="Antwoorden:", value=f"🇦 {antwoord_1}\n🇧 {antwoord_2}\n🇨 {antwoord_3}\n🇩 {antwoord_4}")

        embed.add_field(name="Deze quiz verloopt:", value=disnake.utils.format_dt(time.time() + quiz_sluit_tijd, 'R'), inline=False)

        embed.set_footer(text=f"Quiz ID: {quiz_id}")

        msg = await channel.send(embed=embed)

        await msg.add_reaction("🇦")
        await msg.add_reaction("🇧")
        
        if antwoord_3 != None:
            await msg.add_reaction("🇨")
        if antwoord_4 != None:
            await msg.add_reaction("🇩")

        return msg



    def insert_quiz_in_db(quiz_id, msg_id, quiz_titel, quiz_vraag, antwoord_1, antwoord_2, antwoord_3, antwoord_4, quiz_sluit_tijd):
        Database.cursor.execute("INSERT INTO quizes ()")


def setup(bot: commands.Bot):

    bot.add_cog(Quiz(bot))