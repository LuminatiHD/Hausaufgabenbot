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

database = sqlite3.connect(Itemfile, timeout=10)


class newItem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(help="Trage neue Elemente ein. Die kann man mit 'todo' ansehen und bearbeiten. (Tipp: Mit "
                           "'exit' oder 'stop' kannst du die Erstellung direkt abbrechen)")
    async def new(self, ctx: Context):
        if self.bot.user != ctx.author:
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

# ====================================== DATUM ==================================================
            menu = Buttons.ChooseDatum(ctx)
            menumsg = await ctx.channel.send("Wann ist der Test oder die Aufgabe fällig?", view=menu)
            allaskmessages.append(menumsg)

            while not menu.over:
                menu = Buttons.ChooseDatum(ctx, menu.day, menu.month, menu.year)
                await menumsg.edit(view=menu)
                await menu.wait()

            exitcommand = menu.exit

            for i in menu.children:
                i.disabled = True

            await menumsg.edit(view=menu)

            if not exitcommand:
                date = f"{menu.year}-{int(menu.month):02}-{int(menu.day):02}"

# ======================================== FACH =========================================================

            if not exitcommand:
                allaskmessages.append(await ctx.reply("Welches Fach? "))
                fach = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
                fach = FuncLibrary.changefachname(fach.content)
                exitcommand = fach in ["Break", "Exit", "Stop"] or fach.startswith("!")

# ======================================== AUFGABE =========================================================
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
                await ctx.channel.send("Erstellung wird abgebrochen")

# ========================================= ACCESS =======================================
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

# ====================================== EINTRAGEN =====================================
            if not exitcommand:
                database.cursor().execute(
                    f"INSERT INTO {Itemtable} VALUES (?,?,?,?,?)",
                    (date, category, fach, aufgabe, access))
                await ctx.channel.send(f"{category} wurde eingetragen")
                database.commit()

# ======================================== CLEANUP ==========================================
            for i in allaskmessages:
                await i.delete()


def setup(client):
    client.add_cog(newItem(client))
