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

    @commands.command()
    async def new(self, ctx: Context):
        if self.bot.user != ctx.author and ctx.author not in enteringusers:
            button = Buttons.TestOrHA(ctx)
            await ctx.reply("Welche Itemkategorie soll das Item haben?", view=button)
            await button.wait()
            category = button.choice
            exitcommand = False  # isch da für weme möcht abbräche
            error = True
            while error:
                await ctx.message.reply("Wann ist der Test oder die Aufgabe fällig?")
                try:
                    dateraw = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
                    exitcommand = dateraw.content in ["break", "exit", "stop"]
                    if exitcommand:
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
                await ctx.reply("Welches Fach? ")
                fach = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
                fach = FuncLibrary.changefachname(fach.content)
                exitcommand = fach in ["Break", "Exit", "Stop"]

            if category != "Test" and not exitcommand:
                await ctx.reply("Was zu tun ist: ")
                aufgabe = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
                aufgabe = aufgabe.content
                exitcommand = aufgabe in ["break", "exit", "stop"]

            elif not exitcommand:
                yesno = Buttons.Confirm(ctx)
                await ctx.reply("Schon Lernziele? ", view=yesno)
                await yesno.wait()
                if yesno.confirm:
                    await ctx.reply("Lernziele:")
                    aufgabe = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
                    aufgabe = aufgabe.content
                else:
                    await ctx.reply("Keine aufgabe")
                    aufgabe = None

            if not exitcommand:
                manageaccess = Buttons.ManageItemAccess(ctx)
                await ctx.reply("Für wen soll dieses Item sichtbar sein?", view=manageaccess)
                await manageaccess.wait()
                if manageaccess.access == "all":
                    access = "all"
                elif manageaccess.access == "private":
                    access = ctx.author.id

                else:
                    access = manageaccess.access

            if not exitcommand:
                database.cursor().execute(
                    f"INSERT INTO {Itemtable} VALUES ('{date}', '{category}', '{fach}', '{aufgabe}', '{access}')")
                await ctx.channel.send(f"{category} wurde eingetragen")
                database.commit()


def setup(client):
    client.add_cog(newItem(client))
