import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import sqlite3
import Buttons
import FuncLibrary
from datetime import date, datetime, timedelta, time

Itemfile = "ItemFiles.db"
database = sqlite3.connect(Itemfile)
cs = database.cursor()


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

        if not suggestion.lower() in ["ligma", "sugma", "you suck", "u suck"]:
            confirm = await ctx.channel.send("Wird eingetragen...")
            time = datetime.now()
            time = f"{time.hour:02}:{time.minute:02}:{time.second:02}, {time.day:02}.{time.month:02}.{str(time.year)[-2::]}"
            # ds {time.x:02} isch eifach nur da für weme z.B. ä uhrzit vo 9:16:1 het, dass drus när 09:16:1 wird.
            # So isch ds Layout nicer.

            with open(r"user_feedback.txt", "a") as file:
                file.write(f"\n\n- [{time}] {ctx.author.name}: {suggestion}")

            await confirm.edit(content="Vorschlag wurde eingetragen.")

        else:
            await ctx.reply("Bro häb frässe")

    @commands.command(name="remindme", aliases=["remind"],
                      help="Stelle dir einen Reminder. Für die Zeitangabe, gib die Zeit bitte in der Form HH:MM an."
                           "Der Bot schickt dir dann um diese Uhrzeit einen Reminder.")
    async def set_reminder(self, ctx:Context):
        error = True
        while error:
            await ctx.reply("Wann willst du erinnert werden (Uhrzeit)?")
            timemsg = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)

            try:
                minute = int(timemsg.content.split(':')[1])
                hour = int(timemsg.content.split(":")[0])
                zeit = time(hour=hour, minute=minute)
                error = False

            except IndexError:
                await ctx.reply("Zeit muss in der Form HH:MM angegeben werden")

            except ValueError:
                await ctx.reply("Inkorrekte Eingabe")

        await ctx.reply("An was willst du erinnert werden?")
        reminder = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)

        cs.execute(f"INSERT INTO reminder VALUES ({int(ctx.author.id)}, ?, ?)", (str(zeit), reminder.content))
        database.commit()

        await ctx.channel.send("Reminder wurde eingetragen")

    @commands.command(name="poll", help="Mache Polls. Format ist: !poll [test verschieben] [nicht verschieben]")
    async def poll(self, ctx:Context):
        try:
            optiona = ctx.message.content.split("[")[1].replace("]", "")
            optionb = ctx.message.content.split("[")[2].replace("]", "")

            votebutton = Buttons.VoteButtons(240.0)
            votebutton.OptA.label=optiona
            votebutton.OptB.label = optionb
            vote = await ctx.channel.send("Vote time", view=votebutton)
            await votebutton.wait()

            if votebutton.votes:
                votecounta, votecountb = list(votebutton.votes.values()).count(optiona), list(votebutton.votes.values()).count(optionb)

                if votecounta>votecountb:
                    await vote.reply(f"'{optiona}' hat gewonnen mit {votecounta} zu {votecountb} Punkten!")

                elif votecountb>votecounta:
                    await vote.reply(f"'{optionb}' hat gewonnen mit {votecountb} zu {votecounta} Punkten!")

                else:
                    await vote.reply(f"Es ist Gleichstand ({votecounta}:{votecountb}")

            else:
                await vote.reply("Niemand hat gewählt")

        except IndexError:
            await ctx.reply("Invalide syntax. Optionen müssen in der form [A][B] angegeben werden")

        except nextcord.errors.HTTPException:
            await ctx.reply("Nachricht ist zu lang. Darf nur 80 zeichen lang sein.")

    @commands.command(name="!stcol")
    async def test(self, ctx:Context):
        liste = list(FuncLibrary.StP_colors.keys())
        liste.sort(key=lambda m:FuncLibrary.StP_colors[m])
        for i in liste:
            await ctx.channel.send(embed=nextcord.Embed(title=i, color=FuncLibrary.StP_colors[i]))
        await ctx.channel.send("done")

    @commands.command(name="!memlist")
    async def members(self,ctx:Context):
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


def setup(client):
    client.add_cog(extracmds(client))