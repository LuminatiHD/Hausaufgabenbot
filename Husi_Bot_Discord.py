import asyncio
import discord
from nextcord.ext import commands, tasks
import datetime
import json
import Item
#import main
from Item import newItem, searchItems
import encoding

client = commands.Bot(command_prefix='!')  # , help_command= CustomHelpCommand()


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Hello there!'))
    print('Bot is ready.')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')



@client.command()
async def hw(ctx):
    await ctx.send(f' Was möchtes du machen? \n A: Neue Aufgabe \n B: Neuer Test \n C: outlook \n')

    def check(msg):
        print('hey')
        return msg.content == 'neue aufgabe' or msg.content == 'a'

    msg = await client.wait_for('message', check=check)
    print('msg: ', msg)

    if msg.content == 'neue aufgabe' or msg.content == 'a':
        await ctx.send('hausaufgabe')
        #newItem("Hausaufgabe")

    elif msg.content() == "neuer test" or msg.content() == 'b':
        await ctx.send('test')
        #newItem("Test")












client.run('ODgxNDczNjU2MDUwNTY5MjY3.YStWUA.L-TMGjVXr9G3uo-fGjFwTmrLA8Y')
