import disnake
from disnake.ext import commands, tasks
from env import *
import time
import random
from database import Database
from datetime import datetime, timedelta
import random
import asyncio
# Quiz start tijd: 1 min (static)
# Quiz doorloop tijd: 2.5 minuten

class Quiz(commands.Cog):



    def __init__(self, bot: commands.Bot):

        self.bot = bot
        print("Cog Quiz is loaded!")
        self.ongoing_quizes = []
        self.icons = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫"]
        self.answers_randomized_with_icons = []
        self.quiz_data = {}
        self.quiz_answers_icons = {}
        self.quiz_answers = []
        self.quiz_winners = []
        self.quiz_losers = []



    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):

        if reaction.member == self.bot.user: return
        
        if len(self.quiz_answers) > 0:
            for item in self.quiz_answers:
                if reaction.member.id == item[0]: return
                
        answer_user = [int(reaction.member.id), str(reaction.emoji)]
        self.quiz_answers.append(answer_user)



    # Mother Of All Commands
    @commands.slash_command()
    async def quiz(self, inter):

        pass



    # Quiz make command
    @quiz.sub_command(description="Maak een quiz aan")
    async def aanmaken(self, inter, vraag: str, juiste_antwoord_1: str, verkeerd_antwoord_1: str, 
        juiste_antwoord_2: str = None, verkeerd_antwoord_2: str = None, verkeerd_antwoord_3: str = None, verkeerd_antwoord_4: str = None 
        ):
        
        try:
            
            self.quiz_answers.clear()

            quiz_id = random.randint(0, 6969)

            # Save values in list to randommize        
            i = []
            for item in juiste_antwoord_1, juiste_antwoord_2, verkeerd_antwoord_1, verkeerd_antwoord_2, verkeerd_antwoord_3, verkeerd_antwoord_4:
                if item != None:
                    i.append(item)

            i = random.sample(i, len(i))
            
            icon_count = 0 
            for item in i:
                x = [item, self.icons[icon_count]]
                self.answers_randomized_with_icons.append(x)
                icon_count = icon_count + 1

            # Save right icons to list
            icons_with_right_answer = []
            for item in self.answers_randomized_with_icons:
                if item[0] == juiste_antwoord_1 or item[0] == juiste_antwoord_2:
                    icons_with_right_answer.append(str(item[1]))

            if len(icons_with_right_answer) == 1:
                icons_with_right_answer.append(None)

            # Save quiz data
            self.quiz_data = {
                "quiz_maker": str(inter.author.name),
                "right_answer_1": str(juiste_antwoord_1),
                "right_answer_2": str(juiste_antwoord_2),
                "right_answer_1_icon": icons_with_right_answer[0],
                "right_answer_2_icon": icons_with_right_answer[1],
                "wrong_answer_1": str(verkeerd_antwoord_1),
                "wrong_answer_2": str(verkeerd_antwoord_2),
                "wrong_answer_3": str(verkeerd_antwoord_3),
                "wrong_answer_4": str(verkeerd_antwoord_4)
            }
            
            await Quiz.quiz_embed_starts_over(inter)

            # Wait 60 seconds
            time.sleep(60)
            
            await Quiz.quiz_embed_started(self, inter, quiz_question=vraag)

            # Check for if a user has won
            await Quiz.check_quiz_outcome_thread(self, inter, right_answer_1=juiste_antwoord_1, right_answer_2=juiste_antwoord_2, quiz_answers=self.quiz_answers)


        except Exception as error:
            print(error)
            pass



    async def quiz_embed_starts_over(inter):

        embed=disnake.Embed(title="Quiz tijd!", description=f"Hij start {disnake.utils.format_dt(datetime.now() + timedelta(seconds=60), 'R')}")
        await inter.response.send_message(embed=embed)



    async def quiz_embed_started(self, inter, quiz_question):

        channel = self.bot.get_channel(inter.channel.id)

        embed=disnake.Embed(title=f"Quiz! - {quiz_question}", description=f"Hij verloopt {disnake.utils.format_dt(datetime.now() + timedelta(seconds=150), 'R')}", color=0xdf8cfe)
        embed.add_field(name="Let op!", value="Je 1e antwoord geld! Je reactie verwijderen/wijzigen wordt niet meegerekend! De 1e wint!", inline=False)
        answers = ""

        for item in self.answers_randomized_with_icons:
            answers = answers + f"{item[1]} - {item[0]}\n"

        embed.add_field(name="Antwoorden:", value=f"**{answers}**", inline=False)
        embed.set_footer(text=f"Quiz gemaakt door {inter.author.display_name}")

        msg = await channel.send(embed=embed)

        self.ongoing_quizes.append(int(msg.id))

        for item in self.answers_randomized_with_icons:
            await msg.add_reaction(str(item[1]))

    

    async def check_quiz_outcome_thread(self, inter, right_answer_1, right_answer_2, quiz_answers):

        # Get channel to send
        channel = self.bot.get_channel(inter.channel.id)

        # Wait 2.5 minutes
        await asyncio.sleep(150)

        for quiz_reaction in quiz_answers:
            if quiz_reaction[1] == self.quiz_data["right_answer_1_icon"] or quiz_reaction[1] == self.quiz_data["right_answer_2_icon"]:
                self.quiz_winners.append(int(quiz_reaction[0]))
            else:
                self.quiz_losers.append(int(quiz_reaction[0]))

        if len(self.quiz_winners) > 0:
            embed=disnake.Embed(title=f"Quiz! - We hebben winnaars!", description=f"Aantal deelnemers: {len(self.quiz_winners) + len(self.quiz_losers)}", color=0xdf8cfe)
        else:
            embed=disnake.Embed(title=f"Quiz! - We hebben geen winnaars", description=f"Aantal deelnemers: {len(self.quiz_winners) + len(self.quiz_losers)}", color=0xdf8cfe)

        embed.add_field(name="Voor de spelers:", value="Hoe sneller je bent hoe hoger dichterbij je bij #1 bent.", inline=False)

        if len(self.quiz_winners) == 0:
            embed.add_field(name=f"Er zijn geen winnaars! ", value="\n", inline=False)        

        position_number = 1
        for winner in self.quiz_winners:
            name = (await self.bot.get_or_fetch_user(int(winner))).display_name
            embed.add_field(name=f"#{position_number}", value=str(name), inline=False)
            position_number += 1

        if len(self.quiz_losers) == 0:
            embed.add_field(name=f"Er zijn geen verliezers!", value="\n", inline=False)

        for loser in self.quiz_losers:
            name = (await self.bot.get_or_fetch_user(int(loser))).display_name
            embed.add_field(name=f"Verliezer {position_number}:", value=str(name), inline=False)
            position_number += 1

        await channel.send(embed=embed)

        # Add XP to user
        # Give xp to #1
        if len(self.quiz_winners) > 0:
            Quiz.add_xp_to_winner(player=self.quiz_winners[0], XP=1000)        

        # Save to log
        log_channel = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
        await log_channel.send(f"User {self.quiz_winners[0]} heeft XP gekregen!")


        # End stage
        print("Quiz checking done!")
        

        
        # CLeaning
        self.answers_randomized_with_icons.clear()
        self.quiz_data.clear()
        self.quiz_answers_icons.clear()
        self.quiz_answers.clear()
        self.quiz_winners.clear()
        self.quiz_losers.clear()



    def add_xp_to_winner(player, XP):
        Database.cursor.execute(f"SELECT * FROM Users WHERE id={player} LIMIT 1")
        res = Database.cursor.fetchone()
        Database.cursor.execute(f"UPDATE Users SET xp={int(res[1] + XP)} WHERE id={player}")
        Database.db.commit()
        print(f"User {player} has recieved {XP} XP!")



def setup(bot: commands.Bot):

    bot.add_cog(Quiz(bot))