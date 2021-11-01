import datetime
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import sqlite3
from datetime import date, timedelta
import Buttons

Itemfile = "ItemFiles.db"
Alltables = "testitems", "items"
Itemtable = "items"
tablecategories = ("datum", "kategorie", "fach", "aufgabe", "access", ("rowid"))
Itemkategorien = ("Test", "Aufgabe")

weekdays = ["Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",  # es git vor datetime-library ä command wo tuet dr wuchetag vomne datum zrüggäh,
            "Sonntag"]  # allerdings nur aus integer. Ds isch für ds formatting.

database = sqlite3.connect(Itemfile)


def layout(items, footer):
    week_1 = False
    week_2 = False
    month_1 = False
    month_2 = False
    future = False
    output = nextcord.Embed()
    for item in items:
        (year, month, day) = item[0].split("-")

        if date(int(year), int(month), int(day)) <= date.today() + timedelta(7) and not week_1:  # week_1 teschtet öb ds scho isch vergäh worde, wenn nid de machter das häre
            output.add_field(name="__BIS NÄCHSTE WOCHE:__", value=f"(Bis zum {date.today() + timedelta(7)})",inline=False)
            week_1 = True

        if date.today() + timedelta(7) <= date(int(year), int(month), int(day)) <= date.today() + timedelta(14) and not week_2:
            output.add_field(name="__NÄCHSTE 2 WOCHEN:__", value=f"(Bis zum {date.today() + timedelta(14)})")
            week_2 = True

        if date.today() + timedelta(14) <= date(int(year), int(month), int(day)) <= date.today() + timedelta(30) and not month_1:
            output.add_field(name="__INNERHALB VON 30 TAGEN:__", value=f"(Bis zum {date.today() + timedelta(30)})")
            month_1 = True

        if date.today() + timedelta(30) <= date(int(year), int(month), int(day)) <= date.today() + timedelta(60) and not month_2:
            output.add_field(name="__INNERHALB VON 60 TAGEN:__", value=f"(Bis zum {date.today() + timedelta(60)})")
            month_2 = True

        if date.today() + timedelta(60) <= date(int(year), int(month), int(day)) and not future:
            lastitem = items[-1][0].split("-")
            output.add_field(name="__SPÄTER ALS 60 TAGE:__", value=f"(Bis zum {date(int(lastitem[0]), int(lastitem[1]), int(lastitem[2]))})")
            future = True

        desc = item[3]
        if len(desc)>20:
            desc = item[3][:20]+"..." # wöu schüsch chasch du lernziele ha wo viu ds läng si.

        output.add_field(name=f" {item[1].capitalize()} {item[2]}", value=f" {str(weekdays[date(int(year), int(month), int(day)).weekday()])}, {day}.{month}.{year}\n"
                               f" {desc}\n ", inline=False)
        output.set_footer(text=footer)
    return output


def changefachname(fach):  # so isches übersichtlecher
    fach = fach.capitalize()
    if fach == "Französisch":
        fach = "Franz"
    elif fach == 'Englisch':
        fach = 'English'
    elif fach == 'Biologie':
        fach = 'Bio'
    elif fach == 'Geschichte':
        fach = 'History'

    return fach


class Itemsearch(commands.Cog):
    for item in database.cursor().execute( f"SELECT datum, rowid FROM {Itemtable}"):  # aui elemänt lösche wo scho düre si
        if str(date.today()) > item[0]:
            database.cursor().execute(f"DELETE FROM {Itemtable} WHERE rowid = {item[5]}")
    database.commit()

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def outlook(self, ctx: Context):
        if self.bot.user != ctx.author:
            try:
                EF = "all"
                SF = "all"
                for role in ctx.author.roles:
                    if role.name.lower().startswith("ef"):
                        EF = role.name
                    elif role.name.lower().startswith("sf"):
                        SF = role.name
            except AttributeError:  # für DM-modus
                SF = "all"
                EF = "all"
            search = ctx.message.content[9:]
            if search == "":
                search = None
            items = database.cursor().execute(f"SELECT *, rowid FROM {Itemtable} WHERE access = 'all' OR access = '{ctx.author.id}' OR access = '{SF}' OR access = '{EF}' ORDER BY datum").fetchall()
            results = [i for i in items]  # weme ds nid macht de tuetses bi results.remove ds elemänt bi items ou remove ka werum
            if search is not None:
                for keyword in search.split(", "):
                    for item in items:
                        keyword = changefachname(keyword.capitalize())  # mues für input und output ou so si
                        if keyword.lower().capitalize() not in item and item in results:
                            results.remove(item)
            if results:  # aaschiinend giut ä lääri lischte aus ä boolean, ka bro
                begin = datetime.datetime.now()
                buttons = Buttons.PageButtons(results, 0, ctx)
                currentpage = 0
                selection = results[:5]
                outputmsg = await ctx.reply(embed=layout(selection, footer=f"Seite {1}/{int(len(results) / 5) + (len(results) % 5 > 0)}"),
                                            view=buttons)
                while datetime.datetime.now() < begin + datetime.timedelta(minutes=2):
                    await buttons.wait()  # ds wartet druf das öppis drücket wird. ds geit bim Button mitem self.stop(). Problem isch aber, dass me dr button när nümme cha bruuche, auso muesme ä neue generiere.
                    if buttons.left or buttons.right:  # luegt öb d pagetaschte si drücket worde. schüsch weiser dasme möcht selecte.
                        currentpage = buttons.currentpage

                        selection = results[currentpage * 5:(currentpage + 1) * 5]
                        buttons = Buttons.PageButtons(results, currentpage, ctx)
                        await outputmsg.edit(embed=layout(selection, footer=f"Seite {currentpage + 1}/{int(len(results) / 5) + (len(results) % 5 > 0)}"), view=buttons)  # es isch übersichtlecher, d message ds editiere aus se neu d schicke.

                    else:
                        selecteditem = selection[buttons.select]
                        selected = nextcord.Embed(title=f"{selecteditem[1]} {selecteditem[2]} ")
                        selected.add_field(name="Aufgabe:", value=selecteditem[3], inline=True)
                        selected.add_field(name="Zugriff: ", value=selecteditem[4], inline=True)
                        (year, month, day) = selecteditem[0].split("-")
                        selected.set_footer(text=f"Fällig bis: {str(weekdays[date(int(year), int(month), int(day)).weekday()])}, {day}.{month}.{year}\n")

                        selectbtn = Buttons.Selectionmode(ctx)
                        await outputmsg.edit(embed=selected, view=selectbtn)
                        await selectbtn.wait()  # button.wait() wartet druf dasme öppis het drückt

                        if selectbtn.goback:
                            selection = results[currentpage * 5:(currentpage + 1) * 5]
                            buttons = Buttons.PageButtons(results, currentpage, ctx)
                            await outputmsg.edit(embed=layout(selection, footer=f"Seite {currentpage + 1}/{int(len(results) / 5) + (len(results) % 5 > 0)}"), view=buttons)
                        elif selectbtn.delete:
                            confirm = Buttons.Confirm(ctx)
                            await ctx.reply(content="Willst du wirklich das Item löschen?", view=confirm)
                            await confirm.wait()
                            if confirm.confirm:
                                database.cursor().execute(f"DELETE FROM {Itemtable} WHERE rowid = {selecteditem[5]}")
                                database.commit()
                                await ctx.reply("Item wurde gelöscht")

                        elif selectbtn.edit:
                            editor = await ctx.reply("Was genau möchtest du editieren?")
                            editorbtn = Buttons.EditButtons(ctx)
                            await editor.edit(view=editorbtn)
                            await editorbtn.wait()
                            if "kategorie" in editorbtn.edit:
                                confirm = Buttons.Confirm(ctx)
                                await editor.edit(
                                    content=f"Alte Kategorie ist {selecteditem[1]}. Möchtest du es zu {Itemkategorien[Itemkategorien.index(selecteditem[1]) - 1]} konvertieren?",
                                    view=confirm)
                                await confirm.wait()
                                if confirm.confirm:
                                    database.cursor().execute(f"UPDATE {Itemtable} SET kategorie = '{Itemkategorien[Itemkategorien.index(selecteditem[1]) - 1]}'WHERE rowid = {selecteditem[5]}")

                            if "aufgabe" in editorbtn.edit:
                                confirm = Buttons.Confirm(ctx)
                                while not confirm.confirm:
                                    confirm = Buttons.Confirm(ctx)
                                    await ctx.reply("Aufgabe: ")
                                    newaufg = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author)
                                    await newaufg.reply(f"Alte Aufgabe: {selecteditem[3]}\nNeue Aufgabe: {newaufg.content}.\nBestätigen?", view = confirm)
                                    await confirm.wait()
                                database.cursor().execute(f"UPDATE {Itemtable} SET aufgabe = '{newaufg.content}' WHERE rowid = {selecteditem[5]}")

                            if "datum" in editorbtn.edit:
                                error = True
                                confirm = Buttons.Confirm(ctx)
                                while error and not confirm.confirm:
                                    confirm = Buttons.Confirm(ctx)
                                    await ctx.message.reply("Wann ist der Test oder die Aufgabe fällig?")
                                    try:
                                        dateraw = await self.bot.wait_for("message",
                                                                          check=lambda msg: msg.author == ctx.author)
                                        datum = str(datetime.date(int(dateraw.content.split(".")[2]),
                                                                 int(dateraw.content.split(".")[1]),
                                                                 int(dateraw.content.split(".")[0])))

                                        await dateraw.reply(f"Altes Datum: {selecteditem[0]}\nNeues Datum: {datum}\nBestätigen?", view=confirm)
                                        await confirm.wait()
                                        error = False
                                    except:
                                        await ctx.reply("ungültiges Datum")
                                        continue
                                database.cursor().execute(f"UPDATE {Itemtable} SET datum = '{datum}' WHERE rowid = {selecteditem[5]}")
                            if "fach" in editorbtn.edit:
                                confirm = Buttons.Confirm(ctx)
                                while not confirm.confirm:
                                    confirm = Buttons.Confirm(ctx)
                                    await ctx.reply("Fach: ")
                                    newfach = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)

                                    await newfach.reply(f"Altes Fach: {selecteditem[2]}\nNeues Fach: "
                                                        f"{changefachname(newfach.content)}.\nBestätigen?", view=confirm)
                                    await confirm.wait()
                                database.cursor().execute(
                                    f"UPDATE {Itemtable} SET fach = '{changefachname(newfach.content)}' WHERE rowid = {selecteditem[5]}")

                            if "access" in editorbtn.edit:
                                confirm = Buttons.Confirm(ctx)
                                newacc = Buttons.ManageItemAccess(ctx)
                                while not confirm.confirm:
                                    confirm = Buttons.Confirm(ctx)
                                    await editor.reply("Zugriff: ", view=newacc)
                                    await newacc.wait()

                                    await editor.reply(f"Alter Zugriff: {selecteditem[4]}\nNeuer Zugriff: "
                                                        f"{newacc.access}.\nBestätigen?", view=confirm)
                                    await confirm.wait()
                                database.cursor().execute(
                                    f"UPDATE {Itemtable} SET access = '{newacc.access}' WHERE rowid = {selecteditem[5]}")

                            await ctx.channel.send("Änderungen wurden vorgenommen")
                        database.commit()

            else:
                await ctx.reply("Keine Resultate gefunden.")


def setup(client):
    client.add_cog(Itemsearch(client))
