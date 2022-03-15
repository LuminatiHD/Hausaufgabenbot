import datetime
import sqlite3
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import Buttons
import FuncLibrary

Itemfile = "ItemFiles.db"
Alltables = "items"
Itemtable = "items"
tablecategories = ("datum", "kagegorie", "fach", "aufgabe", "access")

# es git vor datetime-library ä command wo tuet dr wuchetag vomne datum zrüggäh,
# allerdings nur aus integer. Ds isch für ds formatting.

database = sqlite3.connect(Itemfile, timeout=10)


class newItem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(help="Trage neue Elemente ein. Die kann man mit 'todo' ansehen und bearbeiten. (Tipp: Mit "
                           "'exit' oder 'stop' kannst du die Erstellung direkt abbrechen)")
    async def new(self, ctx: Context):
        try:
            faecher = tuple(i for i in ctx.guild.channels
                       if type(i) == nextcord.TextChannel
                        and i.permissions_for(ctx.author).view_channel
                         and self.bot.get_channel(i.category_id).name.lower() == "fächer")

        except AttributeError:
            faecher = tuple()

        if self.bot.user != ctx.author:
            button = Buttons.TestOrHA(ctx)
            categorymsg = await ctx.reply("welche Kategorie?", view=button)

            await button.wait()

            exitcommand = button.exit  # isch da für weme möcht abbräche

            if not exitcommand:
                category = button.choice
            else:
                await categorymsg.delete()
                category = ""
# ====================================== DATUM ==================================================
            if not exitcommand:
                menu = Buttons.ChooseDatum(ctx)

                await categorymsg.edit(content="Wann ist der Test oder die Aufgabe fällig?", view=menu)
                menumsg = categorymsg

                while not menu.over:
                    menu = Buttons.ChooseDatum(ctx, menu.day, menu.month, menu.year)
                    await menumsg.edit(view=menu)
                    await menu.wait()

                exitcommand = menu.exit

                if not exitcommand:
                    date = f"{menu.year}-{int(menu.month):02}-{int(menu.day):02}"

                await menumsg.delete()

# ======================================== FACH =========================================================

            if not exitcommand:
                fach_msg = menumsg
                if faecher:
                    choose = Buttons.Dropdown_Menu(ctx, tuple(i.name for i in faecher)+("andere...",))
                    await fach_msg.edit(content="Welches Fach?", view=choose)
                    await choose.wait()

                    exitcommand = choose.goback
                    if not exitcommand:
                        fach = choose.output[0]

                if not faecher or (locals().get("fach") and fach == "andere..."):
                    fach_msg = await fach_msg.edit(
                        content="Welches Fach? (Schreibe 'break', um die Erstellung abzubrechen)", view=None)

                    fach = await self.bot.wait_for("message",
                                                   check=lambda msg: msg.author == ctx.author and msg.content
                                                                     and not msg.content.startswith("!"))
                    fach = FuncLibrary.changefachname(fach.content)
                    exitcommand = fach in ["Break", "Exit", "Stop"] or fach.startswith("!")

                await fach_msg.delete()
# ======================================== AUFGABE =========================================================
            if category != "Test" and not exitcommand:
                aufg_msg = await ctx.reply("Was zu tun ist:")

                aufgabe = await self.bot.wait_for("message",
                                                  check=lambda msg: msg.author == ctx.author and msg.content)
                aufgabe = aufgabe.content

                exitcommand = aufgabe in ["break", "exit", "stop"] or aufgabe.startswith("!")
                await aufg_msg.delete()

            elif not exitcommand:
                yesno = Buttons.Confirm(ctx)
                asklernziele = await ctx.reply("Schon Lernziele?", view=yesno)
                await yesno.wait()
                await asklernziele.delete()

                if yesno.confirm:
                    aufg_msg = await ctx.reply("Lernziele:")

                    aufgabe = await self.bot.wait_for("message",
                                                      check=lambda msg: msg.author == ctx.author and msg.content)
                    aufgabe = aufgabe.content
                    exitcommand = aufgabe in ["break", "exit", "stop"] or aufgabe.startswith("!")

                    await aufg_msg.delete()
                else:
                    aufgabe = None

# ========================================= ACCESS =======================================
            if not exitcommand:
                manageaccess = Buttons.ManageItemAccess(ctx)
                askaccess_msg = await ctx.reply("Für wen soll dieses Item sichtbar sein?", view=manageaccess)

                await manageaccess.wait()

                if manageaccess.access == "all":
                    access = "all"
                elif manageaccess.access == "private":
                    access = ctx.author.id

                else:
                    access = manageaccess.access

                await askaccess_msg.delete()

# ====================================== EINTRAGEN =====================================
            if not exitcommand:
                database.cursor().execute(
                    f"INSERT INTO {Itemtable} VALUES (?,?,?,?,?)",
                    (date, category, fach, aufgabe, access))

                database.commit()

            await ctx.message.add_reaction("✅")


def setup(client):
    client.add_cog(newItem(client))
