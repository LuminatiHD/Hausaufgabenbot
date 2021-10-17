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


@client.command()
async def new(ctx):
    await ctx.send(f' Was möchtest du machen? \n A: Neue Aufgabe \n B: Neuer Test')
    client.load_extension("cogs.newItem")

    # if msg.content == 'neue aufgabe' or msg.content == 'a':
    #     await ctx.send('Hausaufgabe:')
    #
    # elif msg.content() == "neuer test" or msg.content() == 'b':
    #     await ctx.send('Test:')
    #
    # elif msg.content().lower() == "outlook" or msg.content().lower() == "c":
    #     searchItems(msg, database, search = msg.content().lower()[8:])




client.run('ODk5MjI0MDI1Nzk1MDAyMzY4.YWvpog.s31oLtCJ8TIujHaoYBtZmWXDWu0')
