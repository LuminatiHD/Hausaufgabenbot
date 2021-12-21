import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
from datetime import *
import sqlite3
import Buttons

database = sqlite3.connect("ItemFiles.db")
cs = database.cursor()


class Reminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="remindme", aliases=["remind"],
                      help="Stelle dir einen Reminder. Für die Zeitangabe, gib die Zeit bitte in der Form HH:MM an."
                           "Der Bot schickt dir dann um diese Uhrzeit einen Reminder.")
    async def set_reminder(self, ctx: Context):
        error = True
        while error:
            await ctx.reply("Wann willst du erinnert werden (Uhrzeit)?", delete_after=60)
            timemsg = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)

            try:
                minute = int(timemsg.content.split(':')[1])
                hour = int(timemsg.content.split(":")[0])
                zeit = time(hour=hour, minute=minute)
                error = False

            except IndexError:
                await ctx.reply("Zeit muss in der Form HH:MM angegeben werden", delete_after=60)

            except ValueError:
                await ctx.reply("Inkorrekte Eingabe", delete_after=180)

        await ctx.reply("An was willst du erinnert werden?", delete_after=180)
        reminder = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)

        cs.execute(f"INSERT INTO reminder VALUES ({int(ctx.author.id)}, ?, ?)", (str(zeit), reminder.content))
        database.commit()

        await ctx.channel.send("Reminder wurde eingetragen", delete_after=60)

    @commands.command(name="reminders")
    async def reminderlist(self, ctx:Context):
        allreminders = cs.execute(f"SELECT *, rowid FROM reminder WHERE user_id = {int(ctx.author.id)}").fetchall()

        begin = datetime.now()
        currpage = 0
        outmsg = await ctx.channel.send(content = "ä sec")

        while datetime.now() < begin + timedelta(minutes=2):
            if allreminders:
                output = nextcord.Embed(title=f"Reminder von {ctx.author.name}")

                selection = allreminders[currpage * 5:(currpage + 1) * 5]
                choose = Buttons.PageButtons(allreminders, currpage, ctx)

                for reminder in selection:
                    output.add_field(name=reminder[2], value=reminder[1])

                await outmsg.edit(content=None, embed=output, view=choose)
                await choose.wait()

                if choose.left or choose.right:
                    currpage = choose.currentpage

                elif choose.select > -1:
                    confirm = Buttons.Confirm(ctx)
                    await outmsg.edit(content="Willst du den Reminder wirklich löschen?", view=confirm)
                    await confirm.wait()

                    if confirm:
                        allreminders.remove(selection[choose.select])
                        cs.execute(f"DELETE FROM reminder WHERE rowid = {selection[choose.select][3]}")
                        database.commit()

                else:
                    await outmsg.delete()
                    break

            else:
                await outmsg.edit(content="Wir haben keine Reminder von dir "
                                          "gefunden. Du kannst welche erstellen mit !remindme", view=None, embed=None)


def setup(bot):
    bot.add_cog(Reminders(bot))
