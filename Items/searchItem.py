import datetime
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import sqlite3
from datetime import date
import Buttons
from Items.editItem import editItem
import FuncLibrary
Itemfile = "ItemFiles.db"
Alltables = "items"
Itemtable = "items"
tablecategories = ("datum", "kategorie", "fach", "aufgabe", "access", "rowid")
Itemkategorien = ("Test", "Aufgabe", "")

database = sqlite3.connect(Itemfile)


class Itemsearch(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def outlook(self, ctx: Context):
        # aui Elemänt wo scho düre si wärde glöschet.
        database.cursor().execute(f"DELETE FROM {Itemtable} WHERE datum<?", (str(date.today()),))
        database.commit()
        search = ctx.message.content[len("!outlook "):]
        timeset = str(date.today())
        bfore_or_after = ">="

        if search.startswith("bis") or search.startswith("ab"):
            timeset = search[len("ab "):].split(", ")[0].split(".")
            try:
                timeset = date(int(timeset[2]), int(timeset[1]), int(timeset[0]))
                bfore_or_after = "<=" if search.startswith("bis") else ">="

            except IndexError:
                await ctx.channel.send("Invalider Input. Zeitangaben müssen in der Form \"DD.MM.YY angegeben\" werden.")
                return

            except ValueError:
                await ctx.channel.send("Invalider Input.")
                return
            try:
                search = search[search.index(", "):]
            except ValueError:
                search = None

        ef, sf, kf, mint = FuncLibrary.get_access_permissions(ctx.author)
        items = database.cursor().execute(f"SELECT *, rowid FROM {Itemtable} WHERE datum {bfore_or_after} ? AND (access = 'all' " \
                                          f"OR access = ? OR access = ? "\
                                          f"OR access = ? OR access = ?) ORDER BY datum",
                                          (timeset, ctx.author.id, sf, ef, kf)).fetchall()
        if search == "":
            search = None
        # weme ds nid macht de tuetses bi results.remove ds elemänt bi items ou remove ka werum
        results = [i for i in items]
        if search is not None:
            for keyword in search.split(", "):
                for item in items:
                    keyword = FuncLibrary.changefachname(keyword.capitalize())  # mues für input und output ou so si
                    if keyword.lower().capitalize() not in item and item in results:
                        results.remove(item)
        if results:  # aaschiinend giut ä lääri lischte aus ä boolean, ka bro
            begin = datetime.datetime.now()
            buttons = Buttons.PageButtons(results, 0, ctx)
            currentpage = 0
            selection = results[:5]
            outputmsg = await ctx.reply(embed=FuncLibrary.layout(selection,
                                        footer=f"Seite {1}/{int(len(results) / 5) + (len(results) % 5 > 0)}"),
                                        view=buttons)
            while datetime.datetime.now() < begin + datetime.timedelta(minutes=2):
                # ds wartet druf das öppis drücket wird. ds geit bim Button mitem self.stop(). Problem isch aber,
                # dass me dr button när nümme cha bruuche, auso muesme ä neue generiere.
                await buttons.wait()

                # luegt öb ä pagetaschte isch drücket worde. schüsch weiser dasme möcht selecte.
                if buttons.left or buttons.right:
                    currentpage = buttons.currentpage

                    selection = results[currentpage * 5:(currentpage + 1) * 5]
                    buttons = Buttons.PageButtons(results, currentpage, ctx)

                    # es isch übersichtlecher, d message ds editiere aus se neu d schicke.
                    await outputmsg.edit(embed=FuncLibrary.layout(selection,
                                         footer=f"Seite {currentpage + 1}/{int(len(results) / 5) + (len(results) % 5 > 0)}"),
                                         view=buttons)

                else:
                    selecteditem = selection[buttons.select]
                    # we dr zuegriff aus userid iigspicheret isch, de versuechters z näh.
                    # weses nid geit, isches nid ä userid.
                    try:
                        access = await self.bot.fetch_user(selecteditem[4])
                    except nextcord.errors.HTTPException:
                        access = selecteditem[4]

                    selected = nextcord.Embed(title=f"{selecteditem[1]} {selecteditem[2]} ")
                    selected.add_field(name="Aufgabe:", value=selecteditem[3], inline=False)
                    selected.add_field(name="Zugriff: ", value=access, inline=False)
                    (year, month, day) = selecteditem[0].split("-")
                    selected.set_footer(text=f"Fällig bis: "
                                             f"{str(FuncLibrary.weekdays[date(int(year), int(month), int(day)).weekday()])}, "
                                             f"{day}.{month}.{year}\n")

                    selectbtn = Buttons.Selectionmode(ctx)
                    await outputmsg.edit(embed=selected, view=selectbtn)
                    await selectbtn.wait()  # button.wait() wartet druf dasme öppis het drückt

                    if selectbtn.goback:
                        selection = results[currentpage * 5:(currentpage + 1) * 5]
                        buttons = Buttons.PageButtons(results, currentpage, ctx)
                        await outputmsg.edit(embed=FuncLibrary.layout(selection,
                                             footer=f"Seite {currentpage + 1}/{int(len(results) / 5) + (len(results) % 5 > 0)}"),
                                             view=buttons)
                    elif selectbtn.delete:
                        confirm = Buttons.Confirm(ctx)
                        confirmmsg = await ctx.reply(content="Willst du wirklich das Item löschen?", view=confirm)
                        await confirm.wait()
                        if confirm.confirm:
                            database.cursor().execute(f"DELETE FROM {Itemtable} WHERE rowid = {selecteditem[5]}")
                            database.commit()
                            await confirmmsg.edit(content="Item wurde gelöscht", view=None)

                        elif selectbtn.edit:
                            await editItem(self, ctx, selecteditem)
                        database.commit()

        else:
            await ctx.reply("Keine Resultate gefunden.")


def setup(client):
    client.add_cog(Itemsearch(client))
