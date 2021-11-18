import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import sqlite3

import Buttons
import FuncLibrary
from datetime import date, datetime, timedelta, time

Itemfile = "ItemFiles.db"
database = sqlite3.connect(Itemfile)
cs = database.cursor()


class extracmds(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    # @commands.event
    # async def on_message(self, message):
    #     """isch absolut useless, nur da für fun."""
    #     if message.content in [":(", ":D", "D:", ">:("] and self.bot.user != message.author:
    #         await message.channel.send(message.content)

    @commands.command(name="feedback", aliases=["f"], help="Gib uns Feedback für unseren Bot!")
    async def recommend(self, ctx:Context):

        if ctx.message.content[1:] in ["feedback", "f"]:
            await ctx.channel.send("Feedback: ")
            suggestion = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
            suggestion = suggestion.content
        else:
            suggestion = ctx.message.content[ctx.message.content.index(" "):]

        if not suggestion.lower() in ["ligma", "sugma", "you suck", "u suck"]:
            confirm = await ctx.channel.send("Wird eingetragen...")
            time = datetime.now()
            time = f"{time.hour:02}:{time.minute:02}:{time.second:02}, {time.day:02}.{time.month:02}.{str(time.year)[-2::]}"
            # ds {time.x:02} isch eifach nur da für weme z.B. ä uhrzit vo 9:16:1 het, dass drus när 09:16:1 wird.
            # So isch ds Layout nicer.

            with open(r"user_feedback.txt", "a") as file:
                file.write(f"\n\n- [{time}] {ctx.author.name}: {suggestion}")

            await confirm.edit(content="Vorschlag wurde eingetragen.")

        else:
            await ctx.reply("Bro häb frässe")

    @commands.command(name="remindme", aliases=["remind"],
                      help="Stelle dir einen Reminder. Für die Zeitangabe, gib die Zeit bitte in der Form HH:MM an.")
    async def set_reminder(self, ctx:Context):
        await ctx.reply("Wann willst du erinnert werden (Uhrzeit)?")
        timemsg = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
        minute = int(timemsg.content.split(':')[1])
        hour = int(timemsg.content.split(":")[0])
        zeit = time(hour=hour, minute=minute)

        await ctx.reply("An was willst du erinnert werden?")
        reminder = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)

        cs.execute(f"INSERT INTO reminder VALUES ({int(ctx.author.id)}, ?, ?)", (str(zeit), reminder.content))
        database.commit()

        await ctx.channel.send("Reminder wurde eingetragen")

    @commands.command(name="!stcol")
    async def test(self, ctx:Context):
        liste = list(FuncLibrary.StP_colors.keys())
        liste.sort(key=lambda m:FuncLibrary.StP_colors[m])
        for i in liste:
            await ctx.channel.send(embed=nextcord.Embed(title=i, color=FuncLibrary.StP_colors[i]))
        await ctx.channel.send("done")

    @commands.command(name="!memlist")
    async def members(self,ctx:Context):
        for i in self.bot.guilds[0].members:
            print(f"{i.name:15}{i.id:12}\n"+"-"*40)


def setup(client):
    client.add_cog(extracmds(client))