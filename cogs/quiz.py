import disnake
from disnake.ext import commands, tasks
from env import *
import time
import random
from database import Database
from datetime import datetime, timedelta
import random

# Quiz start tijd: 1 min (static)
# Quiz doorloop tijd: 2.5 minuten

class Quiz(commands.Cog):



    def __init__(self, bot: commands.Bot):

        self.bot = bot
        print("Cog Quiz is loaded!")
        self.ongoing_quizes = []
        self.icons = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫"]
        self.quiz_answers_icons = {}
        self.quiz_answers = {}



    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        if reaction.message.id not in self.ongoing_quizes: return
        
        if user.id == self.bot.user.id: return

        if user.id in self.quiz_answers.keys(): return

        self.quiz_answers[int(user.id)] = {
            "emoticon": str(reaction.emoji)
        }



    # Mother Of All Commands
    @commands.slash_command()
    async def quiz(self, inter):

        pass



    # Quiz make command
    @quiz.sub_command(description="Maak een quiz aan")
    async def aanmaken(self, inter, vraag: str, juiste_antwoord_1: str, verkeerd_antwoord_1: str, 
        juiste_antwoord_2: str = None, verkeerd_antwoord_2: str = None, verkeerd_antwoord_3: str = None, verkeerd_antwoord_4: str = None 
        ):

        # Saving user input in list
        input_values = []
        for item in juiste_antwoord_1, verkeerd_antwoord_1, juiste_antwoord_2, verkeerd_antwoord_2, verkeerd_antwoord_3, verkeerd_antwoord_4:
            if item != None:
                input_values.append(str(item))

        random.shuffle(input_values)

        i = 0
        for item in input_values:
            self.quiz_answers_icons[str(item)] = {"emoji": str(self.icons[i])}
            i = i + 1

        # Send embed quiz starts over 1 minute
        await Quiz.quiz_embed_starts_over(inter)

        # Wait 1 minute (change to 1 min later)
        time.sleep(3)

        await Quiz.quiz_embed_started(self, inter, quiz_question = vraag)

        # wait for quiz to close (2.5 min)
        time.sleep(5)
        
        print(self.quiz_answers_icons)
        
        #check winner
        #for quiz_user in self.quiz_answers.items():
            #if quiz_user[1]["emoticon"]



    async def quiz_embed_starts_over(inter):

        embed=disnake.Embed(title="Quiz tijd!", description=f"Hij start {disnake.utils.format_dt(datetime.now() + timedelta(seconds=60), 'R')}")
        await inter.response.send_message(embed=embed)



    async def quiz_embed_started(self, inter, quiz_question):

        channel = self.bot.get_channel(inter.channel.id)

        embed=disnake.Embed(title=f"Quiz! - {quiz_question}", description=f"Hij verloopt {disnake.utils.format_dt(datetime.now() + timedelta(seconds=150), 'R')}", color=0xdf8cfe)
        embed.add_field(name="Let op!", value="Je 1e antwoord geld! Je reactie verwijderen/wijzigen wordt niet meegerekend! De 1e wint!", inline=False)
        answers = ""

        for item in self.quiz_answers_icons:
            answers = answers + f"{item[0]} - {item[1]}\n"
        embed.add_field(name="Antwoorden:", value=f"**{answers}**", inline=False)
        embed.set_footer(text=f"Quiz gemaakt door {inter.author.display_name}")

        msg = await channel.send(embed=embed)

        self.ongoing_quizes.append(int(msg.id))

        for item in self.quiz_answers_icons:
            await msg.add_reaction(str(item[0]))



def setup(bot: commands.Bot):

    bot.add_cog(Quiz(bot))