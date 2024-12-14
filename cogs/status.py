import disnake
from disnake.ext import commands
import requests
from env import Status as StatusEnv
from uptime_kuma_api import UptimeKumaApi
from helpers.error import Log

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Log.info("Loaded Cog status")

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
            color=0xdf8cfe,
            url="https://uptime.auticodes.nl"
        )
        embed.add_field(
            name="Online",
            value=online,
            inline=True
        )
        embed.add_field(
            name="Latency",
            value=f"`{str(round(self.bot.latency * 1000))}`ms",
            inline=True
        )

        if resp["attributes"]["current_state"] == "starting":
            embed.add_field(
                name="CPU",
                value=f"`{round(resp["attributes"]["resources"]["cpu_absolute"], 3)}`%",
                inline=True
            )
            embed.add_field(
                name="RAM",
                value=f"`{round(Status.bytes_to_mb(resp["attributes"]["resources"]["memory_bytes"]), 3)}`mb",
                inline=True
            )
            embed.add_field(
                name="Netwerk in",
                value=f"`{round(Status.bytes_to_mb(resp["attributes"]["resources"]["network_rx_bytes"]), 3)}`mb",
                inline=True
            )
            embed.add_field(
                name="Netwerk uit",
                value=f"`{round(Status.bytes_to_mb(resp["attributes"]["resources"]["network_tx_bytes"]), 3)}`mb",
                inline=True
            )
            embed.add_field(
                name="Opslag",
                value=f"`{round(Status.bytes_to_mb(resp["attributes"]["resources"]["disk_bytes"]), 3)}`mb",
                inline=False
            )
        await inter.response.send_message(embed=embed)

    @status.sub_command(description="Zie de infrastructuur status")
    async def pagina(self, inter):
        try:
            embed = disnake.Embed(
                title="Uptime pagina",
                description="AllDayTechAndGaming",
                color=0xdf8cfe,
                url="https://uptime.auticodes.nl/status/main"
            )
            embed.add_field(
                name="Website",
                value=f"Uptime in de laatste 24 uur: `{round(Status.get_kuma_monitor_uptime_precentage(self, monitor_id=4, hours=24), 2)}`%.\n Huidige status: `{Status.get_kuma_monitor_current_status(monitor_id=4)}`.",
                inline=False
            )
            embed.add_field(
                name="AllDayBot",
                value=f"Uptime in de laatste 24 uur: `{round(Status.get_kuma_monitor_uptime_precentage(self, monitor_id=11, hours=24), 2)}`%.\n Huidige status: `{Status.get_kuma_monitor_current_status(monitor_id=11)}`.",
                inline=False
            )

            await inter.response.send_message(embed=embed)
        except Exception as error:
            await inter.response.send_message(f"Er ging iets mis! Fout: `{error}`\n<@632677231113666601> ga eens aan het werk joh!")

    def get_kuma_monitor_current_status(monitor_id):
        uptime_kuma = UptimeKumaApi(url=StatusEnv.KUMA_URL)
        uptime_kuma.login(
            StatusEnv.KUMA_USERNAME,
            StatusEnv.KUMA_PASSWORD
        )

        monitor = uptime_kuma.get_monitor_beats(
            monitor_id,
            1
        )

        if monitor[-1]["status"] == 1:
            return 'Online'

        return 'Offline'

    def get_kuma_monitor_uptime_precentage(self, monitor_id, hours):
        uptime_kuma = UptimeKumaApi(url=StatusEnv.KUMA_URL)
        uptime_kuma.login(
            StatusEnv.KUMA_USERNAME,
            StatusEnv.KUMA_PASSWORD
        )

        monitor = uptime_kuma.get_monitor_beats(
            monitor_id,
            hours
        )

        down_count = sum(1 for record in monitor if record["status"] != 1)

        if len(monitor) > 0:
            return float(100 - ((down_count / len(monitor)) * 100))

        return float(0)

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
