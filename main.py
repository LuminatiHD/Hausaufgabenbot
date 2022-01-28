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

Alltables = "items"
Itemtable = "items"
tablecategories = ("datum", "kategorie", "fach", "aufgabe", "access")
Itemfile = "ItemFiles.db"
database = sqlite3.connect(Itemfile)
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
    samed = client.get_user(421756815118958592)

    if TEST_OR_MAIN == "0":
        covid_channel = client.get_guild(688050375747698707).get_channel(929704436538933278)

    try: # we sech dr bot mues reconnecte, denn motzter wöuder d tasks scho gstartet het.
        remind.start()
        download_pdf.start()
        briefing.start()
        news.start()

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
                           (f"%{(datetime.utcnow()+timedelta(hours=1)).hour:02}:00%",))
        if users:
            for user in users:
                await client.get_user(user[0]).send(embed=main.outputbriefing(client.get_user(user[0]), user[1], user[2], user[3], user[4]))


@tasks.loop(seconds=30)
async def remind():
    zeit = (datetime.utcnow()+timedelta(hours=1)).time()
    if TEST_OR_MAIN == "0" and zeit.hour%8==0 and zeit.minute<30:
        covid_channel = client.get_guild(688050375747698707).get_channel(929704436538933278)
        await FuncLibrary.covid_embed(covid_channel, None)


@tasks.loop(hours=6)
async def download_pdf():
    try:
        await Webscraping.weeklypdf(client=client)
    except IndexError:
        print("Website down or other error")

    await client.change_presence(activity=nextcord.Game(name="!help"))


@tasks.loop(hours=1)
async def news():
    if (datetime.utcnow()+timedelta(hours=1)).hour == 10:
        await news_scraper.post_news(client)


client.run(BOT_TOKEN)
