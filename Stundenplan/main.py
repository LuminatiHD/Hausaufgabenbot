import datetime
import sqlite3
from FuncLibrary import get_access_permissions as access
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
from datetime import date, time, timedelta, datetime

Itemfile = r"ItemFiles.db"
database = sqlite3.connect(Itemfile)
standart = "spstand"
week = ("Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag")



cs = database.cursor()
alltimes = []
wochentage = ["Mo", "Di", "Mi", "Do", "Fr"]


def deletetable(user):
    database.cursor().execute(f"DROP TABLE {user}")


def wipetable(user):
    database.cursor().execute(f"DELETE FROM {user}")


def createtable(user):
    database.cursor().execute(f"CREATE TABLE IF NOT EXISTS {user} (weekday TEXT, time TEXT, fach TEXT, room TEXT, teacher TEXT)")
    database.cursor().execute(f"INSERT INTO {user} VALUES SELECT * FROM spstand")
    database.commit()


class Stundenplan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nextlesson", aliases=["nl"])
    async def next(self, ctx:Context):
        zeit = datetime.now().time()
        table = "spstand"
        sf, ef = access(ctx.author)

        output = cs.execute(f"SELECT * FROM {table} WHERE weekday = '{week[date.today().weekday()]}'"\
                            f"AND time > '{datetime.now().time().hour:02}:{datetime.now().time().minute:02}'"\
                            f"AND (access='all' OR access = '{ef}' OR access = '{sf}')").fetchall()


        if output:
            output.sort(key=lambda elem: elem[1])
            output = output[0]
            await ctx.channel.send(output)
        else:
            await ctx.channel.send("Du hast heute keine Lektionen mehr :D")

    @commands.command(name = "tagesplan", aliases = ["t", "T"])
    async def day(self, ctx:Context):
        table = "spstand"
        currdate = date.today()
        sf, ef, kf = access(ctx.author)
        allitems = cs.execute(f"SELECT fach, time, room FROM {table} WHERE weekday = '{wochentage[date.today().weekday()]}'"\
                            f"AND (access='all' OR access = '{ef}' OR access = '{sf}' OR access = '{kf}')").fetchall()

        allitems.sort(key=lambda elem:elem[1])

        output = nextcord.Embed(title=f"{week[currdate.weekday()]}, {currdate.day}.{currdate.month}.{currdate.year}")

        for i in allitems:
            output.add_field(name=i[0], value=f"{i[1]}\n{i[2]}", inline=False)

        await ctx.channel.send(embed=output)


def setup(client):
    client.add_cog(Stundenplan(client))