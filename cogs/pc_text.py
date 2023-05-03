import disnake
from disnake.ext import commands
from env import *
from database import *



class Pc_text(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Pc_Text is loaded!")


        # Commands pc
        @bot.slash_command()
        async def pc(inter):
            pass


        # advice
        @pc.sub_command(description = "Stuur een bericht voor het vragen naar info voor een pc")
        async def advies(inter):

            embed=disnake.Embed(title=f"Pc advies", description=f"""
1. Wat is het budget?
2. Gaat het om een laptop of desktop?
3. Wat ga je met de PC doen? 
-Basis gebruik zoals internet en/of office applicaties.
- Gamen? 
- Streaming?
- Content creation?

Indien desktop: 
4. Wil je de PC zelf bouwen?
5. Wil je alleen advies voor een geconfigureerde PC of heb je ook muis, toetsenbord en beeldscherm nodig?
6. Heb je een voorkeur voor een bepaalde hoeveelheid opslag?
7. Heb je voorkeur voor een AMD of INTEL processor?
8. Heb je voorkeur voor een Intel, AMD of NVIDIA grafische kaart?
9. Wil je een kleine(mini-itx), middelmatige(micro-atx) of grote (ATX of groter) behuizing ?
10. Heb je voorkeur voor een  RGB of een stealth configuratie?
11. Heb je voorkeur voor lucht of waterkoeling?            

            """, color=0xdf8cfe)
            await inter.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Pc_text(bot))