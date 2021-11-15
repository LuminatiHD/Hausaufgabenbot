import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import sqlite3
import FuncLibrary
from datetime import date, datetime, timedelta

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
        time = datetime.now()
        time = f"{time.hour:02}:{time.minute:02}:{time.second:02}, {time.day:02}.{time.month:02}.{str(time.year)[-2::]}"
        # ds {time.x:02} isch eifach nur da für weme z.B. ä uhrzit vo 9:16:1 het, dass drus när 09:16:1 wird.
        # So isch ds Layout nicer.

        with open(r"C:\Users\yoanm\Workspace\Hausaufgabenbot\USERSUGGESTIONS.txt", "a") as file:
            file.write(f"\n\n- [{time}] {ctx.author.name}: {suggestion}")

        await confirm.edit(content="Vorschlag wurde eingetragen.")

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

    @commands.command(name="!test")
    async def test(self,ctx:Context):
        output = nextcord.Embed(title=f"{FuncLibrary.weekdays[date.today().weekday()]}, "
                                      f"{date.today().day}.{date.today().month}.{str(date.today().year)[2:]} "
                                      f"({datetime.now().hour}:{datetime.now().minute})")


        ef, sf, kf, mint = FuncLibrary.get_access_permissions(ctx.author)
        timeset = f"{(date.today()+timedelta(7)).day}:{(date.today()+timedelta(7)).month}:{(date.today()+timedelta(7)).year}"
        items = database.cursor().execute(f"SELECT * FROM items WHERE datum <= ? AND (access = 'all' " \
                                          f"OR access = ? OR access = ? "\
                                          f"OR access = ? OR access = ?) ORDER BY datum",
                                          (timeset, ctx.author.id, sf, ef, kf)).fetchall()

        output.add_field(name="AUFGABEN UND TESTS DIESE WOCHE:", value=f"({timeset})", inline=False)

        if items:
            for item in items:
                desc = item[3]
                if not desc:  # Wenn man keine Lernziele angegeben hat, dann ist desc=None.
                    desc = "Keine Lernziele"

                elif len(desc) > 20:
                    desc = item[3][:20] + "..."  # wöu schüsch chasch du lernziele ha wo viu ds läng si.

                (year, month, day) = item[0].split("-")
                itemdate = date(int(year), int(month), int(day))
                output.add_field(name=f" {item[1].capitalize()} {item[2]}",
                                 value=f" {str(FuncLibrary.weekdays[itemdate.weekday()])}, "
                                       f"{day}.{month}.{year}\n {desc}\n ",
                                 inline=False)

        else:
            output.add_field(name="Es ist nichts zu tun", value="Du kannst mit !new etwas hinzufügen", inline=False)

        output.add_field(name="DER STUNDENPLAN VON HEUTE:", value="\ ")
        currdate = date.today()
        tag = currdate.weekday()
        wochentage = ["Mo", "Di", "Mi", "Do", "Fr"]

        if tag>4:
            tag = (currdate+(timedelta(7)-timedelta(tag))).weekday()

        allitems = cs.execute(f"SELECT fach, time, room FROM Stundenplan_23b WHERE weekday = ?"\
                              " AND (access='all' OR access = ? OR access = ? OR access = ? OR access=?)",\
                              (wochentage[tag], ef, sf, kf, mint)).fetchall()

        allitems.sort(key=lambda elem:elem[1])
        for i in allitems:
            output.add_field(name=i[0], value=f"{i[1]}\n{i[2]}", inline=False)
        await ctx.channel.send(embed=output)


def setup(client):
    client.add_cog(extracmds(client))