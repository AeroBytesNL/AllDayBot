import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database
import re


class configuration(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


        class welcome_modal(disnake.ui.Modal):
            def __init__(self) -> None:
                components = [
                    disnake.ui.TextInput(
                        label="Tekst",
                        placeholder="Gebruik '{}' om de gebruiker te taggen' of '{#kanaal_naam_hier}' om een kanaal te taggen!",
                        custom_id="content",
                        style=disnake.TextInputStyle.paragraph,
                        min_length=5,
                        max_length=2000,
                    ),
                    disnake.ui.TextInput(
                        label="Je naam",
                        placeholder="KelvinCodes als voorbeeld",
                        custom_id="name",
                        style=disnake.TextInputStyle.single_line,
                        min_length=5,
                        max_length=20,
                    ),                    
                ]
                super().__init__(title="Wijzig de welkom tekst!", custom_id="create_tag", components=components)

            async def callback(self, inter: disnake.ModalInteraction) -> None:
                content = inter.text_values["content"]
                author = inter.text_values["name"]
                
                found = re.findall('{(.+?)}', content)

                lst_channels = []
                for thing in found:
                    if "#" in thing:
                        channel_name = str(thing).split("#")[1]
                        print(channel_name)
                        channel = disnake.utils.get(bot.get_all_channels(), name=channel_name)
                        channel_id = channel.id
                        lst_channels.append((channel_name, channel_id))

                for entry in lst_channels:
                    content = content.replace(str("{#" + str(entry[0]) + "}"), str("<#" + str(entry[1]) + ">" ))


                # Check if text in db:
                Database.cursor.execute("SELECT * FROM configuration_text WHERE service='welcome_text'")

                if Database.cursor.fetchone() == None or Database.cursor.fetchone() == []:
                    Database.cursor.execute(f"INSERT INTO configuration_text (service, content, edited_by) VALUES ('welcome_text', '{content}', '{author}')")
                    Database.db.commit()
                else:
                    Database.cursor.execute(f"UPDATE configuration_text SET service='welcome_text', content='{content}', edited_by='{author}'")
                    Database.db.commit()

                await inter.response.send_message(content, ephemeral=True)
                await log_config_actions(inter, type="welkom_tekst")


    


        # Commands
        @bot.slash_command()
        async def config(inter):
            pass


        @config.sub_command(description="Wijzig welkom tekst!")
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def welkom_tekst(inter):
            await inter.response.send_modal(modal=welcome_modal())



        async def log_config_actions(inter, type):

            embed=disnake.Embed(title="\n", description=f"**{inter.author.name} {type}**", color=disnake.Color.dark_green())
            embed.set_author(name=inter.author.name, icon_url=inter.author.avatar)
            embed.add_field(name="Command gebruikt:", value=str(type), inline=False)
            channel_to_send = bot.get_channel(env_variable.ADJE_LOG_CHANNEL_ID)
            await channel_to_send.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(configuration(bot))