import asyncio
import nextcord
from nextcord.ext import commands, tasks
import datetime
import json
from Item import newItem, searchItems
import sqlite3
Itemfile = "ItemFiles.db"
Alltables = "testitems", "items"
Itemtable = "testitems"
tablecategories = ("datum", "kagegorie", "fach", "aufgabe")
database = sqlite3.connect(Itemfile)


client = commands.Bot(command_prefix='!')  # , help_command= CustomHelpCommand()


@client.event
async def on_ready():
    await client.change_presence(status=nextcord.Status.idle, activity=nextcord.Game('Hello there!'))
    print('Bot is ready.')


client.load_extension("cogs.newItem")
client.load_extension("cogs.searchItem")




client.run('ODk5MjI0MDI1Nzk1MDAyMzY4.YWvpog.s31oLtCJ8TIujHaoYBtZmWXDWu0')
