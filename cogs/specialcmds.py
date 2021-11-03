import datetime

import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context


class extracmds(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    # @commands.event
    # async def on_message(self, message):
    #     """isch absolut useless, nur da für fun."""
    #     if message.content in [":(", ":D", "D:", ">:("] and self.bot.user != message.author:
    #         await message.channel.send(message.content)

    @commands.command(name="suggest", aliases=["suggestion", "Suggest", "Suggestion", "S", "s"])
    async def recommend(self, ctx: commands.context.Context):
        """Mit däm command chame vorschläg bringe. die wäre när m textfile USERSUGGESTIONS.txt ufeglade."""
        await ctx.channel.send("Vorschlag: ")

        time = datetime.datetime.now()
        time = f"{time.hour:02}:{time.minute:02}:{time.second:02}, {time.day:02}.{time.month:02}.{str(time.year)[-2::]}"
        # ds {time.x:02} isch eifach nur da für weme z.B. ä uhrzit vo 9:16:1 het, dass drus när 09:16:1 wird.
        # So isch ds Layout nicer.

        suggestion = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)

        with open(r"C:\Users\yoanm\Workspace\Hausaufgabenbot\USERSUGGESTIONS.txt", "a") as file:
            file.write(f"\n\n- [{time}] {ctx.author.name}: {suggestion.content}")

        await ctx.channel.send("Vorschlag wurde eingetragen.")


def setup(client):
    client.add_cog(extracmds(client))