import disnake
from disnake.ext import commands
from env import *
from database import *
import requests 
import json
import xmltodict
from helpers.error import Log

class news(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Loaded Cog news")

    class Confirm(disnake.ui.View):
        def __init__(self, page, url):
            super().__init__(timeout=0)
            self.current_page = page
            self.url = url

        @disnake.ui.button(label="Pagina verder", style=disnake.ButtonStyle.blurple)
        async def confirm(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
            await news.nu_and_tweakers(self, self.url, inter, page=self.current_page + 1)
            self.value = True

        @disnake.ui.button(label="Pagina terug", style=disnake.ButtonStyle.red)
        async def cancel(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
            await news.nu_and_tweakers(self, self.url, inter, page=self.current_page - 1)
            self.value = False

    # Commands 
    @commands.slash_command()
    async def nieuws(self, inter):
        pass

    @nieuws.sub_command(description= "Zie het tech nieuws van nu")
    async def nu(self, inter, pagina:int = 1):
        url = "https://www.nu.nl/rss/Tech"
        await news.nu_and_tweakers(self, url, inter, page=pagina)

    @nieuws.sub_command(description= "Zie het tech nieuws van nu")
    async def tweakers(self, inter, pagina:int = 1):
        url = "http://feeds.feedburner.com/tweakers/mixed"
        await news.nu_and_tweakers(self, url, inter, page=pagina)

    # Functions
    async def nu_and_tweakers(self, url, inter, page):
        pagina = page
        view = news.Confirm(page, url)

        data = requests.get(str(url)).text

        data_dict = xmltodict.parse(data)
        json_data = json.dumps(data_dict)
        json_data = json.loads(json_data)

        if "nu" in url:
            embed=disnake.Embed(title="Nieuws", description="Van Nu.nl", color=0xdf8cfe)
        elif "tweakers" in url:
                embed=disnake.Embed(title="Nieuws", description="Van Tweakers.nl", color=0xdf8cfe)

        count_items = 0

        for item in json_data["rss"]["channel"]["item"]:
            count_items = count_items + 1

        i = 0;
        i = i + 10 * pagina
        p = (pagina+1) * 10

        x = 0

        index = 0

        components=[
            disnake.ui.Button(label="Pagina verder", style=disnake.ButtonStyle.success, custom_id="forward"),
            disnake.ui.Button(label="Pagina terug", style=disnake.ButtonStyle.danger, custom_id="back"),
        ]

        if i >= count_items:
            embed = disnake.Embed(title="Zoveel pagina's hebben we niet.", color=0xdf8cfe)
            await inter.response.send_message(embed=embed, view=view, ephemeral=True)
            return

        while i < p and i < count_items:
            item = json_data["rss"]["channel"]["item"]
            embed.add_field(name=item[i ]["title"], value=str(f"{item[i ]['description'][:70]} \n {item[i]['link']}"), inline=False)
            index = index + 1
            i = i + 1

        embed.set_footer(text=f"Pagina: {pagina}")

        await inter.response.send_message(embed=embed, view=view, ephemeral=True)

    async def tweakers(inter):
        data = requests.get("https://www.nu.nl/rss/Tech").text

def setup(bot: commands.Bot):
    bot.add_cog(news(bot))