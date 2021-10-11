import asyncio
import discord
from discord.ext import commands, tasks
import datetime
import json
import Item
import main
from Item import newItem, searchItems
import encoding

client = commands.Bot(command_prefix='!')  # , help_command= CustomHelpCommand()


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Hello there!'))
    print('Bot is ready.')


@client.command()
async def hey(ctx):
    await ctx.send('hey')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command()
async def hw(ctx):
    main.options()















client.run('ODgxNDczNjU2MDUwNTY5MjY3.YStWUA.L-TMGjVXr9G3uo-fGjFwTmrLA8Y')
