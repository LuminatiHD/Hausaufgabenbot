# IDEAS:
#   -man könnte den Stundenplan mit Buttons konstruieren
#   und wenn man die Knöpfe drückt, dann werden alle kommenden Items für das Fach angezeigt

import nextcord
from nextcord.ext import commands
import sqlite3
Itemfile = "ItemFiles.db"
Alltables = "testitems", "items"
Itemtable = "testitems"
tablecategories = ("datum", "kategorie", "fach", "aufgabe", "access")
database = sqlite3.connect(Itemfile)


client = commands.Bot(command_prefix='!')  # , help_command= CustomHelpCommand()


@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.idle, activity=nextcord.Game('Hello there!'))
    print('Ready')

client.load_extension("Items.newItem")
client.load_extension("Items.searchItem")
client.load_extension("Items.specialcmds")
client.load_extension("Stundenplan.main")

client.run('ODk5MjI0MDI1Nzk1MDAyMzY4.YWvpog.s31oLtCJ8TIujHaoYBtZmWXDWu0')
