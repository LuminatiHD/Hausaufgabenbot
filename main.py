# IDEAS:
#   -man könnte den Stundenplan mit Buttons konstruieren
#   und wenn man die Knöpfe drückt, dann werden alle kommenden Items für das Fach angezeigt

import nextcord
from nextcord.ext import commands
import sqlite3
from nextcord.ext import tasks

Alltables = "items"
Itemtable = "items"
tablecategories = ("datum", "kategorie", "fach", "aufgabe", "access")
Itemfile = "ItemFiles.db"
database = sqlite3.connect(Itemfile)

intents = nextcord.Intents.all()  # ohni ds dörfti dr bot nid user nach id becho.
client = commands.Bot(command_prefix='!', intents=intents)# , help_command= CustomHelpCommand()


@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.online, activity=nextcord.Game('Hello there!'))
    print('Ready')

client.load_extension("Items.newItem")
client.load_extension("Items.searchItem")
client.load_extension("Items.specialcmds")
client.load_extension("Stundenplan.main")

client.run('ODg4MTI0MDc2NjA5MTMwNTY3.YUOIAA.liiiRdLowjlEFTQncyNN9JxNXVY')
