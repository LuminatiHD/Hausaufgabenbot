import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import sqlite3
import Buttons
import FuncLibrary
from datetime import date, datetime, timedelta, time
from News import news_scraper

Itemfile = "ItemFiles.db"
database = sqlite3.connect(Itemfile)
cs = database.cursor()
Itemtable = "items"


class extracmds(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command(name="feedback", aliases=["f"], help="Gib uns Feedback für unseren Bot!")
    async def recommend(self, ctx:Context):

        if ctx.message.content[1:] in ["feedback", "f"]:
            await ctx.channel.send("Feedback: ")
            suggestion = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
            suggestion = suggestion.content
        else:
            suggestion = ctx.message.content[ctx.message.content.index(" "):]

        if not suggestion.lower().replace(" ", "") in ["ligma", "sugma", "you suck", "u suck", "ligmaballs"]:
            confirm = await ctx.channel.send("Wird eingetragen...")
            time = datetime.utcnow()+timedelta(hours=1)
            time = f"{time.hour:02}:{time.minute:02}:{time.second:02}, {time.day:02}.{time.month:02}.{str(time.year)[-2::]}"
            # ds {time.x:02} isch eifach nur da für weme z.B. ä uhrzit vo 9:16:1 het, dass drus när 09:16:1 wird.
            # So isch ds Layout nicer.

            with open(r"user_feedback.txt", "a") as file:
                file.write(f"\n\n- [{time}] {ctx.author.name}: {suggestion}")

            await confirm.edit(content="Vorschlag wurde eingetragen.")

        else:
            await ctx.reply("Bro häb frässe")

    @commands.command(name="poll", help="Mache Polls. Format ist: !poll statement (dauer) [option a] [option b]")
    async def poll(self, ctx:Context):
        try:
            question = ctx.message.content.split("(")[0][len("!poll "):]
            duration = float(ctx.message.content.split("(")[1].split(")")[0])
            options = set(ctx.message.content.replace("]", "").split("[")[1:])

            view = Buttons.Poll_ViewObj(options=options, duration=duration)
            electionmsg = await ctx.channel.send(content=question, view=view)
            await view.wait()

            votes = list(view.voters.values())
            vote_count = dict()

            for i in options:
                amount = str(votes.count(i))
                if not vote_count.get(amount):
                    vote_count[amount] = list()

                vote_count[amount].append(i)

            winner_amount = max(vote_count.keys())
            winner = vote_count[winner_amount]
            del vote_count[winner_amount]

            if int(winner_amount) == 0:
                await ctx.channel.send("Niemand hat gewählt")

            elif len(winner) > 1:
                await ctx.channel.send(f"""Gleichstand. """
                                       f"""'{"', ".join(winner[:-1])}' und '{winner[-1]}' haben je {winner_amount} """
                                       f"""Votes bekommen.""")
            else:
                await ctx.channel.send(f"'{winner[0]}' hat mit {winner_amount} zu "
                                       f"{':'.join([str(votes.count(i)) for i in options if i != winner[0]])} gewonnen")

            await electionmsg.delete()

        except IndexError:
            await ctx.reply("Invalide Syntax. Syntax ist !poll <Frage> (<Dauer>) [<Option>][<Option>][<Option>]...")

        except nextcord.errors.HTTPException:
            await ctx.reply("Nachricht ist zu lang. Darf nur 80 Zeichen lang sein.")

        except ValueError:
            await ctx.reply(f"'{ctx.message.content.split('(')[1].split(')')[0]}' ist keine Zahl")

    @commands.command(name="covidstats", aliases=["stats", "covid", "despair"], help="Gibt covid-stats")
    async def despair_time(self, ctx:Context):
        output = await ctx.channel.send("get COVID data...")
        await FuncLibrary.covid_embed(ctx.channel, 600)
        await output.edit(content="(Wurde gelöscht wegen Spamprävention)", embed=None, view=None)

    @commands.command(name="!stcol")
    async def stcol(self, ctx:Context):
        liste = list(FuncLibrary.StP_colors.keys())
        liste.sort(key=lambda m:FuncLibrary.StP_colors[m])
        for i in liste:
            await ctx.channel.send(embed=nextcord.Embed(title=i, color=FuncLibrary.StP_colors[i]))
        await ctx.channel.send("done")

    @commands.command(name="!brief")
    async def briefing(self, ctx:Context):
        await ctx.channel.send(embed=FuncLibrary.outputbriefing(ctx.author, "all", "all", "all", "all"))

    @commands.command(name="!memlist")
    async def members(self, ctx:Context):
        for i in self.bot.guilds[0].members:
            print(f"{i.name:15}{i.id:12}\n"+"-"*40)

    @commands.command(name="!sus")
    async def sussy(self, ctx:Context):
        await ctx.reply("STOP POSTING ABOUT AMONG US! I'M TIRED OF SEEING IT! "
                        "MY FRIENDS ON TIKTOK SEND ME MEMES, ON DISCORD IT'S "
                        "FUCKING MEMES! I was in a server, right? and ALL OF "
                        "THE CHANNELS were just among us stuff. I-I showed"
                        " my champion underwear to my girlfriend and t-the logo "
                        "I flipped it and I said \"hey babe, when the underwear is sus HAHA "
                        "DING DING DING DING DING DING DING DI DI DING\" I fucking "
                        "looked at a trashcan and said \"THAT'S A BIT SUSSY\" I looked "
                        "at my penis I think of an astronauts helmet and I go \"PENIS? MORE "
                        "LIKE PENSUS\" AAAAAAAAAAAAAAHGESFG")

    @commands.command(name="!test")
    async def test(self, ctx:Context):
        pass


def setup(client):
    client.add_cog(extracmds(client))
