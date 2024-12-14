import disnake
from disnake.ext import commands
from env import *
from mcstatus import JavaServer
import re
from rcon.source import Client
from env import secure
from helpers.error import Log

class minecraft(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot 
        Log.info("Loaded Cog minecraft")

    # Mother Off All Commands
    @commands.slash_command()
    async def minecraft(self, inter):
        pass

    # Server commands
    @minecraft.sub_command(description="Zie de survival info")
    async def survival_info(self, inter):
        try:
            # General info
            server = JavaServer.lookup(Minecraft.MINECRAFT_DOMAIN)
            status = server.status()

            # PLayers name info with RCON
            with Client(Minecraft.MINECRAFT_DOMAIN, 25575, passwd=Minecraft.MINECRAFT_RCON_PW) as client:
                resp = client.run("list")

            i = re.sub("§.{1}", "", resp)   
            if "\n" in i:
                i = i.split("\n")
            del i[0]

            await minecraft.server_info_embed(self, inter, status, resp=i)
        except Exception as error:
            await inter.response.send_message(f"Error: {error}")

    # Server commands
    @minecraft.sub_command(description="Zie de skyblock info")
    async def skyblock_info(self, inter):
        try:
            # General info
            server = JavaServer.lookup(Minecraft.MINECRAFT_DOMAIN)
            status = server.status()

            # PLayers name info with RCON
            with Client(Minecraft.MINECRAFT_DOMAIN, 25576, passwd=Minecraft.MINECRAFT_RCON_PW) as client:
                resp = client.run("list")

            i = re.sub("§.{1}", "", resp)
            if "\n" in i:
                i = i.split("\n")
            del i[0]

            await minecraft.server_info_embed(self, inter, status, resp=i)
        except Exception as error:
            await inter.response.send_message(f"Error: {error}")

    # Functions
    async def server_info_embed(self, inter, status, resp):
        print(f"Debug 69: ", resp)

        guild = await self.bot.fetch_guild(env_variable.GUILD_ID)
        
        embed=disnake.Embed(title="AllDayTech&Gaming Minecraft", description="Informatie", color=0xdf8cfe)
        embed.add_field(name="Aantal spelers online:", value=str(status.players.online), inline=True)
        embed.add_field(name="Aantal spelers maximaal:", value=str(status.players.max), inline=True)
        
        admin_storage = ""
        moderator_storage = ""
        member_storage = ""

        for item in resp:
            if "beheerder" in item:
                print("83")
                print(item)
                item = item.split(": ", 1)[1]
                users = item.split(" ")

                for user in users:
                    if "," in user:
                        user = user.replace(",", "")

                    user_without_prefix = user.split("Beheerder]")[1]
                    admin_storage = admin_storage + f"{user_without_prefix}\n"

            if "moderator" in item:
                print("95")
                item = item.split(": ", 1)[1]
                users = item.split(" ")

                for user in users:
                    if "," in user:
                        user = user.replace(",", "")

                    user_without_prefix = user.split("Mod]")[1]
                    moderator_storage = moderator_storage + f"{user_without_prefix}\n"
                    
            if "default" in item:
                print("106")
                item = item.split(": ", 1)[1]
                users = item.split(" ")

                for user in users:
                    if "," in user:
                        user = user.replace(",", "")

                    user_without_prefix = user.split("Lid]")[1]
                    member_storage = member_storage + f"{user_without_prefix}\n"

        if len(admin_storage) == 0:
            admin_storage = "Er zijn geen admins online."
        if len(moderator_storage) == 0:
            moderator_storage = "Er zijn geen moderators online."
        if len(member_storage) == 0:
            member_storage = "Er zijn geen leden online."
        
        embed.add_field(name="Admins online:", value=str(admin_storage), inline=False)
        embed.add_field(name="Moderators online:", value=str(moderator_storage), inline=False)
        embed.add_field(name="Leden online:", value=str(member_storage), inline=False)

        embed.set_thumbnail(url=guild.icon)
        await inter.response.send_message(embed=embed)

        admin_storage = ""
        moderator_storage = ""
        member_storage = ""

def setup(bot: commands.Bot):
    bot.add_cog(minecraft(bot))