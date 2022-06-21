import nextcord
from nextcord.ext import commands
import sqlite3
from nextcord.ext import tasks
from datetime import date, datetime, timedelta, time
import help_command
from Briefing import main
import FuncLibrary
from Mensa import Webscraping
from News import news_scraper
import traceback
from time import sleep

Alltables = "items"
Itemtable = "items"
tablecategories = ("datum", "kategorie", "fach", "aufgabe", "access")
Itemfile = "ItemFiles.db"
db_timeout = 10
database = sqlite3.connect(Itemfile, timeout=db_timeout)
cs = database.cursor()


intents = nextcord.Intents.all()  # ohni ds dörfti dr bot nid user nach id becho.
client = commands.Bot(command_prefix='!', intents=intents)
client.help_command = help_command.Help()

with open("TOKEN.txt", "r") as file:
    TEST_OR_MAIN = input("Main [0] or Test [1]? ")
    if TEST_OR_MAIN == "0":
        BOT_TOKEN = file.readlines()[0][len("main: "):]

    else:
        BOT_TOKEN = file.readlines()[1][len("test: "):]


@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.online)
    print('Ready')

    if TEST_OR_MAIN == "0":
        covid_channel = client.get_guild(688050375747698707).get_channel(929704436538933278)

    try: # we sech dr bot mues reconnecte denn motzter wöuder d tasks scho gstartet het.
        covid.start()
        briefing.start()
        news.start()
        remind_task.start()

    except RuntimeError:
        pass

    finally:
        await  client.change_presence(activity=nextcord.Game(name="!help"))

client.load_extension("Items.newItem")
client.load_extension("Items.searchItem")
client.load_extension("Items.specialcmds")
client.load_extension("Stundenplan.main")
client.load_extension("Briefing.main")
client.load_extension("Mensa.main")


@tasks.loop(minutes = 10)
async def briefing():
    if datetime.now().minute//10 ==0:
        zeit = (datetime.now()+timedelta(hours=24-17)).date()
        weekdays = ["mo", "di", "mi", "do", "fr", "sa", "so"]
        users = cs.execute(f"SELECT user_id, sf, ef, kf, mint FROM briefing WHERE "\
                           f"{weekdays[zeit.weekday()]} LIKE ?",
                           (f"%{(datetime.utcnow()+timedelta(hours=2)).hour:02}:00%",))
        if users:
            for user in users:
                await client.get_user(user[0]).send(embed=main.outputbriefing(client.get_user(user[0]), user[1], user[2], user[3], user[4]))


@tasks.loop(hours=6)
async def covid():
    zeit = (datetime.utcnow()+timedelta(hours=2)).time()
    if TEST_OR_MAIN == "0" and zeit.hour%8==0 and zeit.minute<30:
        covid_channel = client.get_guild(688050375747698707).get_channel(929704436538933278)
        await FuncLibrary.covid_embed(covid_channel, 3600*24*2)


@tasks.loop(hours=12)
async def remind_task():
    then = (datetime.utcnow() + timedelta(hours=2))
    cs.execute("DELETE FROM items WHERE datum < ?", (str(then.date()),))
    database.commit()

    for i in cs.execute("SELECT * FROM items WHERE datum <= ?", (str((then+timedelta(days=7)).date()), )).fetchall():
        date = i[0].split('-')
        date = datetime(date[0], date[1], date[2], 0, 0, 0)
        if (date-then).days ==7 or (date-then).days <= 1:
            if i[4].isnumeric():
                channel = client.get_user(int(i[4]))
            else:
                channel = FuncLibrary.get_channel(client.guilds[0], i[2])
                if not channel:
                    channel = client.get_channel(912264818516430849)

            embed = nextcord.Embed(color=0x64d7fa, title=f"{i[1].upper()} AM {date.day}.{date.month}.{date.year}:")\
                .add_field(name="Fach:", value=i[2])\
                .add_field(name="Aufgabe:", value=i[3] if i[3] else "keine angegeben :(")

            if channel:
                await channel.send(embed=embed)


@tasks.loop(hours=1)
async def news():
    if (datetime.utcnow()+timedelta(hours=2)).hour == 10:
        await news_scraper.post_news(client, timedelta(days=1))


@client.event
async def on_command_error(ctx:commands.context.Context, error:Exception):
    """Error Handler."""
    if not type(error) == nextcord.ext.commands.CommandNotFound:
        now = datetime.utcnow() + timedelta(hours=2)
        print("\n"+"="*100+f"\nError from {now.day}.{now.month}.{now.year} on {now.hour:02}:{now.minute:02}:{now.second:02}")
        sleep(0.001) # without this, the error message occasionally gets sent before the timestamp (idk why)
        traceback.print_exception(error)
        # prints the exception with a timestamp

        # sends a notification to LuminatiHD
        owner = client.get_user(633733324447416331)
        out = nextcord.Embed(
            title=f"Error from {now.day}.{now.month}.{now.year} on {now.hour:02}:{now.minute:02}:{now.second:02}",
            description=FuncLibrary.linebreaks(error.args[0], n=40),
            colour=int("7d0410", 16)) \
            .add_field(name="message:", value=ctx.message.content, inline=False) \
            .add_field(name="author:",  value=ctx.author.display_name, inline=False)\
            .add_field(name="channel:", value=ctx.channel, inline=False)

        # if the ctx is in a DM-channel, then specifying the server makes no sense.
        if type(ctx.channel) != nextcord.DMChannel:
            out.add_field(name="guild:", value=ctx.guild.name, inline=False)
        await owner.send(embed=out)

    else:
        await ctx.message.add_reaction("❓")
        await ctx.channel.send("I don't know this command. Type '!help' to see all available commands.")

client.run(BOT_TOKEN)
