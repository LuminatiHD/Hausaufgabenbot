from Mensa import  Webscraping
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
from datetime import date, timedelta
wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]

embedcol = [0xba2929, 0xeb7c28, 0xd6aa18, 0x237a06, 0x086fcf]


class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="menu", aliases=["Menu", "m", "M"], help="Gibt das heutige Menu in der Mensa zurück")
    async def menu(self, ctx:Context):
        datum = date.today()
        if datum.weekday() > 4:
            datum += timedelta(7-datum.weekday())
            print(datum)

        output = await ctx.channel.send("Eine Sekunde...")
        menu = nextcord.Embed(title=f"{wochentage[datum.weekday()]}, "
                                    f"{datum.day}.{datum.month}.{datum.year}",
                              colour = embedcol[datum.weekday()])

        for item in Webscraping.menuoutput(output):
            title = f"{item['title']}"
            if item["label"] in ["vegan", "vegetarian"]:
                if item["label"] == "vegetarian":
                    item["label"] = "vegetarisch"
                title +=f" ({item['label'].upper()})"
            menu.add_field(name=title, value=item["desc"])

        await ctx.channel.send(embed=menu)
        await output.delete()

    @commands.command(name = "wochenplan", aliases=["Wochenplan", "wp", "WP"], help="Gibt das Menu der momentanen Woche zurück")
    async def weekly(self, ctx:Context):
        datum = date.today()
        output = await ctx.channel.send("Einen Moment...")
        weekm = await Webscraping.menuweekly(output)
        await output.edit(content="Verarbeitung komplett...")
        for i in range(len(weekm)//3):
            length = len(weekm)//3
            elem = await ctx.channel.send(f"Element {i+1}/{length+1}")

            if datum.weekday() >4:
                datum = datum+(timedelta(7)-timedelta(datum.weekday()))

            menuoutput = nextcord.Embed(title=f"{wochentage[datum.weekday()%5]}, {datum.day}.{datum.month}.{datum.year}",
                                        color=embedcol[datum.weekday()%5])

            for item in weekm[3*i:3*(i+1)]:
                menuoutput.add_field(name=f"{item['title']} ({item['label'].upper()})" if item["label"] else f"{item['title']}", value=item["desc"])

            await elem.edit(content=None, embed=menuoutput)
            datum = datum + timedelta(1)

        await output.delete()

    @commands.command(name = "wochepdf", aliases=["Wocheypdf", "wpdf", "WPDF", "Wpdf"],
                      help="Gibt ein PDF des momentanen Mensa-Wochenplan zurück.")
    async def weeklypdf(self, ctx:Context):
        output = await ctx.channel.send(content="Einen Moment...")
        await ctx.channel.send(content="Das PDF ist manchmal outdated.", file=nextcord.File(r"Mensa/menu.png"))
        await output.delete()


def setup(client):
    client.add_cog(Menu(client))