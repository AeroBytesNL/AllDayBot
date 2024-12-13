import disnake
from disnake.ext import commands
import requests
from env import Status as StatusEnv

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Status is loaded!")

    @commands.slash_command()
    async def status(self, inter):
        pass

    @status.sub_command(description="Zie de status van AllDayBot")
    async def alldaybot(self, inter):
        resp = Status.get_ptero_api_response("/client/servers/" + StatusEnv.BOT_ID + "/resources")

        if resp["attributes"]["current_state"] == "starting":
            online = "Ja"
        else:
            online = "Nee"

        embed = disnake.Embed(
            title="AllDayBot",
            description="uptime en resource informatie",
            color=disnake.Colour.green(),
            url="https://uptime.auticodes.nl"
        )

        embed.add_field(
            name="Online",
            value=online,
            inline=False
        )

        if resp["attributes"]["current_state"] == "starting":
            embed.add_field(
                name="CPU",
                value=f"{round(resp["attributes"]["resources"]["cpu_absolute"], 3)}%",
                inline=False
            )
            embed.add_field(
                name="RAM",
                value=f"{round(Status.bytes_to_mb(resp["attributes"]["resources"]["memory_bytes"]), 3)}mb",
                inline=False
            )
            embed.add_field(
                name="Opslag",
                value=f"{round(Status.bytes_to_mb(resp["attributes"]["resources"]["disk_bytes"]), 3)}mb",
                inline=False
            )
            embed.add_field(
                name="Netwerk in",
                value=f"{round(Status.bytes_to_mb(resp["attributes"]["resources"]["network_rx_bytes"]), 3)}mb",
                inline=False
            )
            embed.add_field(
                name="Netwerk uit",
                value=f"{round(Status.bytes_to_mb(resp["attributes"]["resources"]["network_tx_bytes"]), 3)}mb",
                inline=False
            )
        await inter.response.send_message(embed=embed)

    def bytes_to_mb(bytes):
        return int(bytes) / (1024 * 1024)

    def get_ptero_api_response(url):
        url = StatusEnv.URL + url
        headers = {
            "Authorization": "Bearer " + StatusEnv.PTERODACTYL_API_TOKEN,
            "Content-Type": "application/json",
            "Accept": "Application/vnd.pterodactyl.v1+json"
        }

        response = requests.get(url, headers=headers)

        if response.ok:
            return response.json()

def setup(bot: commands.Bot):
    bot.add_cog(Status(bot))
