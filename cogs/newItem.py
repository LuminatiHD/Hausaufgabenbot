import datetime
import sqlite3
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import Buttons
Itemfile = "ItemFiles.db"
Alltables = "testitems", "items"
Itemtable = "testitems"
tablecategories = ("datum", "kagegorie", "fach", "aufgabe")

weekdays = ["Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",
            "Sonntag"]  # es git vor datetime-library ä command wo tuet dr wuchetag vomne datum zrüggäh,
                        # allerdings nur aus integer. Ds isch für ds formatting.

database = sqlite3.connect(Itemfile)

enteringusers = []  # da drmit sech d lüt nid gägesiitig düe sache gäh


def changefachname(fach):  # so isches übersichtlecher
    fach = fach.content.capitalize()
    if fach == "Französisch":
        fach = "Franz"
    elif fach == 'Englisch':
        fach = 'English'
    elif fach == 'Biologie':
        fach = 'Bio'
    elif fach == 'Geschichte':
        fach = 'History'

    return fach


def layout(item):
    (year, month, day) = item[0].split("-")

    return f"\n{str(weekdays[datetime.date(int(year), int(month), int(day)).weekday()])}, {day}.{month}.{year}\n" \
           f"{item[1].capitalize()} {item[2]}" \
           f"\n{item[3]}\n"

    # ersti zile git wuchetag sowie datum zrügg.
    # die 2ti git kategorie und fach zrügg (kategorie isch entweder "Test" oder "Hausaufgabe")
    # die 3tti git d ufgab zrügg (oder d lernziu weses ä tescht isch)

    # wägem formatting isches so, dass d datebank d ä output aus liste zrüggbringt.
    # aso wemer üs d datebank aus tabäue vorsteue, de git üs d datebank für nes bestimmts item fougendes use:
    #   [{spaute 1}, {spaute 2}, {spaute 3}...]

    # I üsem fau isch das:
    #   [Itemid, datum, kategorie, fach, ufgab].


class newItem(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command()
    async def new(self, ctx:Context):
        if self.bot.user != ctx.author and ctx.author not in enteringusers:
            button = Buttons.TestOrHA(ctx)
            await ctx.reply("Was möchtest du machen?\nA: Neue Aufgabe\nB: Neuer Test", view = button)
            await button.wait()
            category = button.choice
            exitcommand = False # isch da für weme möcht abbräche
            error = True
            while error:
                await ctx.message.reply("Wann ist der Test oder die Aufgabe fällig?")
                try:
                    dateraw = await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author)
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
                fach = changefachname(await self.bot.wait_for("message", check = lambda msg: msg.author == ctx.author))
                exitcommand = fach in ["Break", "Exit", "Stop"]

            if category == "Hausaufgabe" and not exitcommand:
                await ctx.reply("Aufgabe: ")
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
                database.cursor().execute(f"INSERT INTO {Itemtable} VALUES ('{date}', '{category}', '{fach}', '{aufgabe}')")
                await ctx.channel.send(f"{category} wurde eingetragen")
                database.commit()


def setup(client):
    client.add_cog(newItem(client))
