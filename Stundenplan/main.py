import datetime
import sqlite3

import FuncLibrary
from FuncLibrary import get_access_permissions as access
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
from datetime import date, time, timedelta, datetime

Itemfile = r"ItemFiles.db"
database = sqlite3.connect(Itemfile)
table = "Stundenplan_23b"
week = ("Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag")
weekcol = [0xba2929, 0xeb7c28, 0xd6aa18, 0x237a06, 0x086fcf]
cs = database.cursor()
alltimes = []
wochentage = ["Mo", "Di", "Mi", "Do", "Fr"]


class Stundenplan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nextlesson", aliases=["nl"],
                      help="Gibt einem die nächste Lektion zurück, falls heue noch welche anstehen.")
    async def next(self, ctx:Context):
        tag = datetime.now()
        zeit = tag.time()
        sf, ef, kf, mint= access(ctx.author)

        if not date.today().weekday() in wochentage:
            await ctx.channel.send("Es ist Wochenende, du hast heute keine Lektionen mehr")
            return
        
        output = cs.execute(f"SELECT fach, time, room, teacher  FROM {table} WHERE weekday = ?"\
                            f"AND time > ?"\
                            f"AND (access='all' OR access = ? OR access = ? OR access = ? "
                            f"OR access = ?) ORDER BY time",
                            (wochentage[tag.weekday()],
                             f'{zeit.hour:02}:{zeit.minute:02}-{zeit.hour:02}:{zeit.minute:02}',
                             ef, sf, kf, mint)).fetchone()

        if output:
            zeit = output[1].split("-")[0]
            zeit = datetime.combine(date.today(),
                                     time(int(zeit.split(":")[0]), int(zeit.split(":")[1])))-datetime.now()

            hours = zeit.seconds//3600
            minutes = (zeit.seconds//60)%60
            color = FuncLibrary.StP_colors[output[0].lower()] if output[0].lower() in FuncLibrary.StP_colors.keys() else None

            outputembed = nextcord.Embed(title=output[0], colour=color)

            outputembed.set_footer(text=f"In {minutes} minuten." if not hours else f"In {hours} stunden und {minutes} minuten.")

            if output[2]:
                outputembed.add_field(name="Zimmer:", value=output[2])
            if output[3]:
                outputembed.add_field(name="Lehrperson:", value=output[3])

            await ctx.channel.send(embed=outputembed)

        else:
            await ctx.channel.send("Du hast heute keine Lektionen mehr :D")

    @commands.command(name = "tagesplan", aliases = ["t", "T"], help="Gibt alle heutigen Lektionen zurück.")
    async def day(self, ctx:Context):
        table = "Stundenplan_23b"
        currdate = date.today()
        tag = currdate.weekday()

        if tag<=4:
            sf, ef, kf, mint = access(ctx.author)

            allitems = cs.execute(f"SELECT fach, time, room FROM {table} WHERE weekday = ?"\
                                  " AND (access='all' OR access = ? OR access = ? OR access = ? OR access=?)",\
                                  (wochentage[tag], ef, sf, kf, mint)).fetchall()

            allitems.sort(key=lambda elem:elem[1])

            output = nextcord.Embed(title=f"{week[currdate.weekday()]}, {currdate.day}.{currdate.month}.{currdate.year}",
                                    color=weekcol[tag])

            for i in allitems:
                output.add_field(name=i[0], value=f"{i[1]}\n{i[2]}", inline=False)

            await ctx.channel.send(embed=output)

        else:
            await ctx.channel.send("Es ist Wochenende.")


def setup(client):
    client.add_cog(Stundenplan(client))