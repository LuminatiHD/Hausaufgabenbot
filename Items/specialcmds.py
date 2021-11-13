import datetime
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context

import FuncLibrary


class extracmds(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    # @commands.event
    # async def on_message(self, message):
    #     """isch absolut useless, nur da für fun."""
    #     if message.content in [":(", ":D", "D:", ">:("] and self.bot.user != message.author:
    #         await message.channel.send(message.content)

    @commands.command(name="suggest", aliases=["suggestion", "Suggest", "Suggestion", "S", "s"])
    async def recommend(self, ctx:Context):
        """Mit däm command chame vorschläg bringe. die wäre när m textfile USERSUGGESTIONS.txt ufeglade."""

        if ctx.message.content[1:] in ["suggestion", "Suggest", "Suggestion", "S", "s", "suggest"]:
            await ctx.channel.send("Vorschlag: ")
            suggestion = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
            suggestion = suggestion.content
        else:
            suggestion = ctx.message.content[ctx.message.content.index(" "):]

        confirm = await ctx.channel.send("Wird eingetragen...")
        time = datetime.datetime.now()
        time = f"{time.hour:02}:{time.minute:02}:{time.second:02}, {time.day:02}.{time.month:02}.{str(time.year)[-2::]}"
        # ds {time.x:02} isch eifach nur da für weme z.B. ä uhrzit vo 9:16:1 het, dass drus när 09:16:1 wird.
        # So isch ds Layout nicer.

        with open(r"C:\Users\yoanm\Workspace\Hausaufgabenbot\USERSUGGESTIONS.txt", "a") as file:
            file.write(f"\n\n- [{time}] {ctx.author.name}: {suggestion}")

        await confirm.edit(content="Vorschlag wurde eingetragen.")

    @commands.command(name="!test")
    async def test(self, ctx:Context):
        liste = list(FuncLibrary.StP_colors.keys())
        liste.sort(key=lambda m:FuncLibrary.StP_colors[m])
        for i in liste:
            await ctx.channel.send(embed=nextcord.Embed(title=i, color=FuncLibrary.StP_colors[i]))
        await ctx.channel.send("done")


def setup(client):
    client.add_cog(extracmds(client))