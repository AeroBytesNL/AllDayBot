import disnake
from disnake.ext import commands, tasks
from env import *
import time
import random
from database import Database
from datetime import datetime, timedelta
import random
import asyncio
from helpers.error import Log

# Quiz start tijd: 1 min (static)
# Quiz doorloop tijd: 1.5 minuten

class Quiz(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ongoing_quizes = []
        self.quiz_maker = 0
        self.icons = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫"]
        self.answers_randomized_with_icons = []
        self.quiz_data = {}
        self.quiz_answers_icons = []
        self.quiz_answers = []
        self.quiz_winners = []
        self.quiz_losers = []
        Log.info("Loaded Cog quiz")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        # Do nothing if user is bot
        if reaction.member == self.bot.user: return
        
        # Do nothing if quiz isn't running
        if reaction.message_id not in self.ongoing_quizes: return

        # If there is a reaction and user has already responded: do nothing
        if len(self.quiz_answers) > 0:
            for item in self.quiz_answers:
                if reaction.member.id == item[0]: return

        # If reaction is from quiz_maker then remove it
        if reaction.member.id == self.quiz_maker:
            msg = self.bot.get_message(reaction.message_id)
            await msg.remove_reaction(reaction.emoji, await self.bot.get_or_fetch_user(reaction.member.id))
            return
        
        # If icon is not in the icon list delete it
        if str(reaction.emoji) not in self.quiz_answers_icons:
            msg = self.bot.get_message(reaction.message_id)
            await msg.remove_reaction(reaction.emoji, await self.bot.get_or_fetch_user(reaction.member.id))
            return
        
        # Add reaction from user to list
        answer_user = [int(reaction.member.id), str(reaction.emoji)]
        self.quiz_answers.append(answer_user)

    # Mother Of All Commands
    @commands.slash_command()
    async def quiz(self, inter):
        pass

    # Quiz info command
    @quiz.sub_command(description="Zie info over de quiz!")
    async def info(self, inter):
        embed=disnake.Embed(title="Quiz informatie", description="\n", color=0xdf8cfe)
        embed.add_field(name=f"Regels:", value="""
- De 1e die het juiste antwoord aanklikt wint de quiz.                        
- Je kunt geen quiz aanmaken terwijl een andere quiz nog loopt.
- Je kunt zelf niet reageren (reacties worden automatisch verwijderd.
- Emojis die niet in de quiz zitten worden automatisch verwijderd.
- Tot 2 antwoorden kunnen juist zijn! Tot 4 onjuiste antwoorden mogelijk.                
- Als winnaar op plaats #1 krijg je 1000XP.
- Elke verliezer verliest 1000XP.
- Wanneer je een icoon aanklikt staat je reactie vast!""", inline=True)
        await inter.response.send_message(embed=embed, ephemeral=True)

    # Quiz make command
    @quiz.sub_command(description="Maak een quiz aan")
    async def aanmaken(self, inter, vraag: str, juiste_antwoord_1: str, verkeerd_antwoord_1: str, 
        juiste_antwoord_2: str = None, verkeerd_antwoord_2: str = None, verkeerd_antwoord_3: str = None, verkeerd_antwoord_4: str = None 
        ):
        self.quiz_maker = inter.author.id

        if len(self.ongoing_quizes) > 0:
            await inter.response.send_message("Je kunt geen 2e quiz maken, de 1e quiz is nog bezig!", ephemeral=True)
            return

        self.quiz_answers.clear()

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

        for item in self.answers_randomized_with_icons:
            self.quiz_answers_icons.append(item[1])

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
        
        await Quiz.quiz_embed_starts_over(self, inter)

        # Wait 60 seconds
        time.sleep(60)
        
        await Quiz.quiz_embed_started(self, inter, quiz_question=vraag)
        
        # Wait 2.5 minutes
        await asyncio.sleep(90)

        # Check for if a user has won
        await Quiz.check_quiz_outcome_thread(self, inter, right_answer_1=juiste_antwoord_1, right_answer_2=juiste_antwoord_2, quiz_answers=self.quiz_answers)

        # Clear data
        Quiz.clear_data(self)

    # Quiz score command
    @quiz.sub_command(description="Zie de quiz scorebord!")
    async def scorebord(self, inter):
        await Quiz.quiz_scoreboard(inter, self)

    async def quiz_embed_starts_over(self, inter):
        channel = self.bot.get_channel(inter.channel.id)

        embed=disnake.Embed(title="Quiz tijd!", description=f"Hij start {disnake.utils.format_dt(datetime.now() + timedelta(seconds=60), 'R')}", color=0xdf8cfe)
        embed.add_field(name=f"Regels:", value="""
- Je kunt geen quiz aanmaken terwijl een andere quiz nog loopt.
- Je kunt zelf niet reageren (reacties worden automatisch verwijderd.
- Emojis die niet in de quiz zitten worden automatisch verwijderd.
- Tot 2 antwoorden kunnen juist zijn! Tot 4 onjuiste antwoorden mogelijk.                
- Als winnaar op plaats #1 krijg je 1000 XP.
- Elke verliezer verliest 1000 XP.
- Wanneer je een icoon aanklikt staat je reactie vast!""", inline=True)      
        embed.set_footer(text=f"Quiz gemaakt door {inter.author.display_name}")
        await inter.response.send_message("Quiz is aangemaakt!", ephemeral=True)
        await channel.send(embed=embed)

    async def quiz_embed_started(self, inter, quiz_question):
        channel = self.bot.get_channel(inter.channel.id)

        embed=disnake.Embed(title=f"Quiz! - {quiz_question}", description=f"Hij verloopt {disnake.utils.format_dt(datetime.now() + timedelta(seconds=90), 'R')}", color=0xdf8cfe)
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

        for quiz_reaction in quiz_answers:
            if quiz_reaction[1] == self.quiz_data["right_answer_1_icon"] or quiz_reaction[1] == self.quiz_data["right_answer_2_icon"]:
                self.quiz_winners.append(int(quiz_reaction[0]))
            else:
                self.quiz_losers.append(int(quiz_reaction[0]))

        if len(self.quiz_winners) > 0:
            embed=disnake.Embed(title=f"Quiz! - We hebben winnaars!", description=f"Aantal deelnemers: {len(self.quiz_winners) + len(self.quiz_losers)}", color=0xdf8cfe)
            
            if self.quiz_data["right_answer_2"] != "None":
                embed.add_field(name=f"Juiste antwoorden waren: ", value=f"**- {self.quiz_data['right_answer_1']}\n- {self.quiz_data['right_answer_2']}**", inline=False)        
            else:
                embed.add_field(name=f"Juiste antwoord was: ", value=f"**- {self.quiz_data['right_answer_1']}**", inline=False)       

        else:
            embed=disnake.Embed(title=f"Quiz! - We hebben geen winnaars", description=f"Aantal deelnemers: {len(self.quiz_winners) + len(self.quiz_losers)}", color=0xdf8cfe)

        if len(self.quiz_losers) == 0:
            embed.add_field(name=f"Er zijn geen verliezers!", value="\n", inline=False)

        if len(self.quiz_winners) == 0:
            embed.add_field(name=f"Er zijn geen winnaars! ", value="\n", inline=False)     
            if self.quiz_data["right_answer_2"] != "None":
                embed.add_field(name=f"Juiste antwoorden waren: ", value=f"**- {self.quiz_data['right_answer_1']}\n- {self.quiz_data['right_answer_2']}**", inline=False)        
            else:
                embed.add_field(name=f"Juiste antwoord was: ", value=f"**- {self.quiz_data['right_answer_1']}**", inline=False)        

        position_number = 1
        for winner in self.quiz_winners:
            if position_number == 1:
                Quiz.save_winner_to_db(user_id=winner)

            name = (await self.bot.get_or_fetch_user(int(winner))).display_name
            embed.add_field(name=f"Winnaar #{position_number}", value=str(name), inline=False)
            position_number += 1

        loser_postion_number = 1
        for loser in self.quiz_losers:
            name = (await self.bot.get_or_fetch_user(int(loser))).display_name
            embed.add_field(name=f"Verliezer #{loser_postion_number}:", value=str(name), inline=False)
            loser_postion_number += 1

        await channel.send(embed=embed)

        # Add XP to user
        # Give xp to #1
        if len(self.quiz_winners) > 0:
            Quiz.add_xp_to_winner(player=self.quiz_winners[0], XP=1000)        
            # Save quiz winner to DB

        # Removes XP from losers
        if len(self.quiz_winners) > 0:
            for loser in self.quiz_losers:
                Quiz.remove_xp_from_losers(player=loser, XP=1000)
                
        # Save to log
        if len(self.quiz_winners) > 0:
            log_channel = self.bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await log_channel.send(f"Quiz - User {self.quiz_winners[0]} heeft XP gekregen!")

        # End stage
        print("Quiz checking done!")

    def add_xp_to_winner(player, XP):
        Database.cursor.execute(f"SELECT * FROM Users WHERE id={player} LIMIT 1")
        res = Database.cursor.fetchone()
        Database.cursor.execute(f"UPDATE Users SET xp={int(res[1] + XP)} WHERE id={player}")
        Database.db.commit()
        print(f"Quiz - User {player} has recieved {XP} XP!")

    def remove_xp_from_losers(player, XP):
        Database.cursor.execute(f"SELECT * FROM Users WHERE id={player} LIMIT 1")
        res = Database.cursor.fetchone()
        Database.cursor.execute(f"UPDATE Users SET xp={int(res[1] - XP)} WHERE id={player}")
        Database.db.commit()
        print(f"Quiz - User {player} has got removed {XP} XP!")

    def save_winner_to_db(user_id):
        Database.cursor.execute(f"SELECT * FROM quiz WHERE user_id={user_id} LIMIT 1")
        res = Database.cursor.fetchone()    
        if Database.cursor.rowcount == 0:
            Database.cursor.execute(f"INSERT INTO quiz (win_count, user_id) VALUES (1, {user_id})")
        else:
            Database.cursor.execute(f"UPDATE quiz SET win_count={res[0] + 1} WHERE user_id = {user_id}")
        
        Database.db.commit()

    async def quiz_scoreboard(inter, self):
        Database.cursor.execute("SELECT user_id, win_count FROM quiz ORDER BY win_count DESC")
        res = Database.cursor.fetchall()

        embed = disnake.Embed(title='ADT&G Quiz scorebord', color=0xdf8cfe)
        
        position_count = 1
        for entry in res:
            user = await self.bot.get_or_fetch_user(entry[0])
            embed.add_field(name=f"#{position_count}", value=f"**{user.display_name}**", inline=False)
            position_count += 1
        await inter.response.send_message(embed=embed)

    def clear_data(self):
        # Cleaning
        self.ongoing_quizes.clear()
        self.answers_randomized_with_icons.clear()
        self.quiz_data.clear()
        self.quiz_answers_icons.clear()
        self.quiz_answers.clear()
        self.quiz_winners.clear()
        self.quiz_losers.clear()
        self.quiz_maker = 0

def setup(bot: commands.Bot):
    bot.add_cog(Quiz(bot))