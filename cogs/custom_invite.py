from enum import verify

from disnake.ext import commands, tasks
from helpers.error import Log
import requests
from env import DirectAdmin

class CustomInvite(commands.Cog):
    def __init__(self, bot: commands.Bot):
        Log.info("Cog CustomInvite is loaded!")

    # @commands.slash_command(description="Maak een eigen custom invite aan!")
    # async def invite(self, inter, url:str):
    # try:
    #     url = f"{DirectAdmin.SERVER_URL}/CMD_REDIRECT"
    #
    #     payload = {
    #         "action": "add",
    #         "domain": DirectAdmin.DOMAIN,
    #         "from": "/test",
    #         "to": f"{DirectAdmin.DOMAIN}/efwfwjl",
    #         "type": DirectAdmin.REDIRECT_TYPE,
    #     }
    #
    #     response = requests.post(
    #         url,
    #         data=payload,
    #         auth=(
    #             DirectAdmin.USERNAME,
    #             DirectAdmin.PASSWORD
    #         ),
    #         verify=True
    #     )
    #
    #     response.raise_for_status()
    # except Exception as error:
    #     Log.error(error)

def setup(bot: commands.Bot):
    bot.add_cog(CustomInvite(bot))
