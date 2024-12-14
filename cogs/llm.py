import disnake
from disnake.ext import commands, tasks
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import google.generativeai as genai
from env import Api

class Llm(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("LLM Cog loaded!")

    @commands.slash_command()
    async def ai(self, inter):
        pass

    @ai.sub_command(description="Stel vragen aan Llama-3.3-70B-Instruct")
    async def llama(self, inter, vraag: str):
        channel = self.bot.get_channel(inter.channel.id)
        message = await inter.response.send_message(f"Ik ben aan het denken!...", ephemeral=True)

        client = ChatCompletionsClient(
            endpoint="https://models.inference.ai.azure.com",
            credential=AzureKeyCredential(Api.GH_TOKEN),
        )

        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content=str(vraag)),
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model="Llama-3.3-70B-Instruct"
        )

        await channel.send(content=f"# Llama\n\n ## Vraag:\n{vraag}\n## Antwoord: \n{response.choices[0].message.content}")

    @ai.sub_command(description="Stel vragen aan Gemini!")
    async def gemini(self, inter, vraag: str):
        genai.configure(api_key=Api.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        channel = self.bot.get_channel(inter.channel.id)
        message = await inter.response.send_message(f"Ik ben aan het denken!...", ephemeral=True)
        response = model.generate_content(str(vraag))

        await channel.send(f"# Gemini\n\n ## Vraag:\n{vraag}\n## Antwoord: \n{response.text}")

def setup(bot: commands.Bot):
    bot.add_cog(Llm(bot))