import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import sqlite3
from datetime import date, timedelta
Itemfile = "ItemFiles.db"
Alltables = "testitems", "items"
Itemtable = "testitems"
tablecategories = ("datum", "kagegorie", "fach", "aufgabe")

weekdays = ["Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag", # es git vor datetime-library ä command wo tuet dr wuchetag vomne datum zrüggäh,
            "Sonntag"]  # allerdings nur aus integer. Ds isch für ds formatting.

database = sqlite3.connect(Itemfile)


def layout(items):
    week_1 = False
    week_2 = False
    month_1 = False
    month_2 = False
    future = False
    output = nextcord.Embed()
    for item in items:
        (year, month, day) = item[0].split("-")

        if date(int(year), int(month), int(day)) <= date.today()+timedelta(7) and not week_1: # week_1 teschtet öb ds scho isch vergäh worde, wenn nid de machter das häre
            output.add_field(name="__Bis nächste Woche:__", value=f"(Bis zum {date.today()+timedelta(7)})", inline=False)
            week_1 = True

        if date.today()+timedelta(7) <= date(int(year), int(month), int(day)) <= date.today()+timedelta(14) and not week_2:
            output.add_field(name="__Nächste 2 Wochen:__", value=f"(Bis zum {date.today()+timedelta(14)}")
            week_2 = True

        if date.today()+timedelta(14) <= date(int(year), int(month), int(day)) <= date.today()+timedelta(30) and not month_1:
            output.add_field(name="__Innerhalb von 30 Tagen:__", value=f"(Bis zum {date.today()+timedelta(30)}")
            month_1 = True

        if date.today()+timedelta(30) <= date(int(year), int(month), int(day)) <= date.today()+timedelta(60) and not month_2:
            output.add_field(name="__Innerhalb von 60 Tagen:__", value=f"(Bis zum {date.today()+timedelta(60)}")
            month_2 = True

        if date.today()+timedelta(60) <=date(int(year), int(month), int(day)) and not future:
            lastitem = items[-1][0].split("-")
            output.add_field(name="__Später als 60 Tage:__", value=f"(Bis zum {date(int(lastitem[0]), int(lastitem[1]), int(lastitem[2]))}")
            future = True

        output.add_field(name=f" {item[1].capitalize()} {item[2]}", value=f" {str(weekdays[date(int(year), int(month), int(day)).weekday()])}, {day}.{month}.{year}\n"
                                                                       f" {item[3]}\n ", inline=False)
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
    for item in database.cursor().execute(f"SELECT datum, rowid FROM {Itemtable}"): # aui elemänt lösche wo scho düre si
        if str(date.today()) > item[0]:
            database.cursor().execute(f"DELETE FROM {Itemtable} WHERE rowid = {item[1]}")
    database.commit()

    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command()
    async def outlook(self, ctx:Context):
        if self.bot.user != ctx.author:
            await ctx.reply("Suchparameter: ")
            search = await self.bot.wait_for("message", check = lambda msg:msg.author == ctx.author)
            search = search.content
            results = []
            items = database.cursor().execute(f"SELECT * FROM {Itemtable} ORDER BY datum").fetchall()


            if search == "all":
                results = items

            else:
                for keyword in search.split(", "):
                    for item in items:
                        keyword = changefachname(keyword.capitalize())  # mues für input und output ou so si
                        if keyword.lower().capitalize() in item and item not in results:
                            results.append(item)

            if results: # aaschiinend giut ä lääri lischte aus ä boolean, ka bro
                await ctx.reply(embed=layout(results))
            elif ctx.message.content not in ["!outlook", "!new"]:  # programm het irgendwie problem drmit gha, dueses mau so fixe, wirde hoffentlech no meh luege
                await ctx.reply("Keine resultate gefunden")


def setup(client):
    client.add_cog(Itemsearch(client))