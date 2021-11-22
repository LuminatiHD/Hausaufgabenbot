from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import nextcord
import sqlite3
import Buttons
from Buttons import ChooseWeekdays, ChooseTime, choose_EF, choose_KF, choose_SF, Confirm
import FuncLibrary
from Briefing import editsettings

database = sqlite3.connect("ItemFiles.db")
table = "briefing"
tableschema = "user_id, mo, di, mi, do , fr, sa, so"
week = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
cs = database.cursor()


class Briefing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="briefing", help="Mit briefing kannst du sagen, ob und wann dir der Bot ein Briefing zur "
                                            "kommenden Woche schickt.")
    async def briefing(self, ctx:Context):
        settingsoutput = nextcord.Embed(title="Einstellungen")
        settings = cs.execute("SELECT  mo, di, mi, do, fr, sa, so FROM briefing WHERE user_id=?", (ctx.author.id,)).fetchall()
        if settings:
            settings = settings[0]

            for i in range(len(settings)):
                if settings[i]:
                    zeiten=settings[i][1:-1].replace(",", "\n").replace("'", "")
                    settingsoutput.add_field(name=FuncLibrary.weekdays[i], value=zeiten)

            access = cs.execute("SELECT sf, ef, kf, mint FROM briefing WHERE user_id=?", (ctx.author.id,)).fetchall()[0]
            settingsoutput.add_field(name="SF:", value=access[0])
            settingsoutput.add_field(name="EF:", value=access[1])
            settingsoutput.add_field(name="KF:", value=access[2])

            if access[3] == "all":
                settingsoutput.add_field(name="MINT:", value="Nein")
            else:
                settingsoutput.add_field(name="MINT:", value="Ja")

            askbutton = Buttons.BriefingSettings(ctx)
            output = await ctx.channel.send(embed=settingsoutput, view=askbutton)
            await askbutton.wait()

            for i in askbutton.children:
                i.disabled = True

            await output.edit(view=askbutton)

            if askbutton.choice == "time":
                await editsettings.editdates(ctx)

            elif askbutton.choice == "classes":
                await editsettings.edit_classes(ctx)

        else:
            yesno = Buttons.Confirm(ctx)

            output = await ctx.reply(embed = nextcord.Embed(title="Du hast noch nichts eingestellt",
                                                   description="Möchtest du das ändern?"), view=yesno)
            await yesno.wait()

            if yesno.confirm:
                for i in yesno.children:
                    i.disabled = True
                await output.edit(view = yesno)

                await editsettings.editdates(ctx)
                await editsettings.edit_classes(ctx)


def setup(client):
    client.add_cog(Briefing(client))
