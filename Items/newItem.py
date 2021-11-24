import datetime
import sqlite3
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import Buttons
import FuncLibrary
Itemfile = "ItemFiles.db"
Alltables = "items"
Itemtable = "items"
tablecategories = ("datum", "kagegorie", "fach", "aufgabe", "access")

# es git vor datetime-library ä command wo tuet dr wuchetag vomne datum zrüggäh,
# allerdings nur aus integer. Ds isch für ds formatting.

database = sqlite3.connect(Itemfile)

enteringusers = []  # da drmit sech d lüt nid gägesiitig düe sache gäh


class newItem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(help="Trage neue Elemente ein. Die kann man mit 'todo' ansehen und bearbeiten. (Tipp: Mit "
                           "'exit' oder 'stop' kannst du die Erstellung direkt abbrechen)")
    async def new(self, ctx: Context):
        if self.bot.user != ctx.author and ctx.author not in enteringusers:
            allaskmessages = []

            button = Buttons.TestOrHA(ctx)
            categorymsg = await ctx.reply("welche Kategorie?", view=button)

            await button.wait()
            category = button.choice

            for i in button.children:
                i.disabled = True
            await categorymsg.edit(view=button)

            allaskmessages.append(categorymsg)

            exitcommand = False  # isch da für weme möcht abbräche
            exitoutput = False

            error = True
            while error:
                allaskmessages.append(await ctx.reply("Wann ist der Test oder die Aufgabe fällig?"))

                try:
                    dateraw = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
                    exitcommand = dateraw.content in ["break", "exit", "stop"] or dateraw.content.startswith("!")

                    if exitcommand:
                        await ctx.reply("Erstellung wird abgebrochen")
                        exitoutput = True
                        error = False
                        break

                    date = str(datetime.date(int(dateraw.content.split(".")[2]),
                                             int(dateraw.content.split(".")[1]),
                                             int(dateraw.content.split(".")[0])))
                    # datetime.date nimmt daten nur in der Form YY/MM/DD an
                    error = False
                except (ValueError, IndexError):  # IndexError wöu ja dr input no gsplittet und indexet wird.
                    await ctx.reply("ungültiges Datum")
                    continue
                    # fragt nachemne valid input bis ä valid input gäh wird.

            if not exitcommand:
                allaskmessages.append(await ctx.reply("Welches Fach? "))
                fach = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
                fach = FuncLibrary.changefachname(fach.content)
                exitcommand = fach in ["Break", "Exit", "Stop"] or fach.startswith("!")

            if category != "Test" and not exitcommand:
                allaskmessages.append(await ctx.reply("Was zu tun ist: "))

                aufgabe = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
                aufgabe = aufgabe.content

                exitcommand = aufgabe in ["break", "exit", "stop"] or aufgabe.startswith("!")

            elif not exitcommand:
                yesno = Buttons.Confirm(ctx)
                asklernziele = await ctx.reply("Schon Lernziele? ", view=yesno)

                await yesno.wait()
                for i in yesno.children:
                    i.disabled = True

                await asklernziele.edit(view=yesno)
                allaskmessages.append(asklernziele)

                if yesno.confirm:
                    allaskmessages.append(await ctx.reply("Lernziele:"))

                    aufgabe = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
                    aufgabe = aufgabe.content
                    exitcommand = aufgabe in ["break", "exit", "stop"] or aufgabe.startswith("!")
                else:
                    aufgabe = None

            elif exitcommand and not exitoutput:
                await ctx.reply("Erstellung wird abgebrochen")

            if not exitcommand:
                manageaccess = Buttons.ManageItemAccess(ctx)
                askaccess_msg = await ctx.reply("Für wen soll dieses Item sichtbar sein?", view=manageaccess)
                await manageaccess.wait()

                if manageaccess.access == "all":
                    access = "all"
                elif manageaccess.access == "private":
                    access = ctx.author.id

                else:
                    access = manageaccess.access

                for i in manageaccess.children:
                    i.disabled = True

                await askaccess_msg.edit(view=manageaccess)

                allaskmessages.append(askaccess_msg)

            if not exitcommand:
                database.cursor().execute(
                    f"INSERT INTO {Itemtable} VALUES (?,?,?,?,?)",
                    (date, category, fach, aufgabe, access))
                await ctx.channel.send(f"{category} wurde eingetragen")
                database.commit()

            for i in allaskmessages:
                await i.delete()

def setup(client):
    client.add_cog(newItem(client))
