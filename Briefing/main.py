from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import nextcord
import sqlite3
import Buttons
from Buttons import ChooseWeekdays, ChooseTime, choose_EF, choose_KF, choose_SF, Confirm
from datetime import date, datetime, timedelta
import FuncLibrary
from Briefing import editsettings

database = sqlite3.connect("ItemFiles.db")
table = "briefing"
tableschema = "user_id, mo, di, mi, do , fr, sa, so"
week = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
cs = database.cursor()


class Briefing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="briefing", help="Mit briefing kannst du sagen, ob und wann dir der Bot ein Briefing zur "
                                            "kommenden Woche schickt.")
    async def briefing(self, ctx:Context):
        settingsoutput = nextcord.Embed(title="Einstellungen")
        settings = cs.execute("SELECT  mo, di, mi, do, fr, sa, so FROM briefing WHERE user_id=?", (ctx.author.id,)).fetchall()
        if settings:
            settings = settings[0]

            for i in range(len(settings)):
                if settings[i]:
                    zeiten=settings[i][1:-1].replace(",", "\n").replace("'", "")
                    settingsoutput.add_field(name=FuncLibrary.weekdays[i], value=zeiten)

            access = cs.execute("SELECT sf, ef, kf, mint FROM briefing WHERE user_id=?", (ctx.author.id,)).fetchall()[0]
            settingsoutput.add_field(name="SF:", value=access[0])
            settingsoutput.add_field(name="EF:", value=access[1])
            settingsoutput.add_field(name="KF:", value=access[2])

            if access[3] == "all":
                settingsoutput.add_field(name="MINT:", value="Nein")
            else:
                settingsoutput.add_field(name="MINT:", value="Ja")

            askbutton = Buttons.BriefingSettings(ctx)
            output = await ctx.channel.send(embed=settingsoutput, view=askbutton)
            await askbutton.wait()

            await output.delete()

            if askbutton.choice == "time":
                await editsettings.editdates(ctx)

            elif askbutton.choice == "classes":
                await editsettings.edit_classes(ctx)

        else:
            yesno = Buttons.Confirm(ctx)

            output = await ctx.reply(embed = nextcord.Embed(title="Du hast noch nichts eingestellt",
                                                   description="Möchtest du das ändern?"), view=yesno)
            await yesno.wait()

            if yesno.confirm:
                for i in yesno.children:
                    i.disabled = True
                await output.edit(view = yesno)

                await editsettings.editdates(ctx)
                await editsettings.edit_classes(ctx)


def setup(client):
    client.add_cog(Briefing(client))


def outputbriefing(user, ef, sf, kf, mint):
    weekdays = FuncLibrary.weekdays
    today = (datetime.utcnow()+timedelta(hours=1))
    output = nextcord.Embed(title=f"{weekdays[today.weekday()]}, "
                                  f"{today.day}.{today.month}.{str(today.year)[2:]} "
                                  f"({today.hour}:{today.minute:02})")

    timeset = today+timedelta(days=7)
    items = cs.execute(f"SELECT * FROM items WHERE datum <= ? AND (access = 'all' " \
                                      f"OR access = ? OR access = ? " \
                                      f"OR access = ? OR access = ?) ORDER BY datum",
                                      (timeset, user.id, sf, ef, kf)).fetchall()

    output.add_field(name="AUFGABEN UND TESTS DIESE WOCHE:",
                     value=f"(Bis {timeset.day}.{timeset.month}.{timeset.year})", inline=False)

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
                             value=f" {str(weekdays[itemdate.weekday()])}, "
                                   f"{day}.{month}.{year}\n {desc}\n ",
                             inline=False)

    else:
        output.add_field(name="Es ist nichts zu tun", value="Du kannst mit !new etwas hinzufügen.", inline=False)

    currdate = (datetime.now()+timedelta(hours=24-17)).date()
    tag = currdate.weekday()
    wochentage = ["Mo", "Di", "Mi", "Do", "Fr"]

    if tag > 4:
        tag = (currdate + (timedelta(7) - timedelta(tag))).weekday() # tag wird ufe mänti gsetzt
        output.add_field(name=".", value="**DER STUNDENPLAN VON MONTAG:**")

    elif currdate == date.today():
        output.add_field(name=".", value="**DER STUNDENPLAN VON HEUTE:**")

    else:
        output.add_field(name=".", value="**DER STUNDENPLAN VON MORGEN**")

    allitems = cs.execute(f"SELECT fach, time, room FROM Stundenplan_23b WHERE weekday = ?" \
                          " AND (access='all' OR access = ? OR access = ? OR access = ? OR access=?)", \
                          (wochentage[tag], ef, sf, kf, mint)).fetchall()

    allitems.sort(key=lambda elem: elem[1])
    for i in allitems:
        output.add_field(name=i[0], value=f"{i[1]}\n{i[2]}", inline=False)
    return output
