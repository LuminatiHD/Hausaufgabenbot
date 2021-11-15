from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import nextcord
import sqlite3
from Buttons import ChooseWeekdays, ChooseTime, choose_EF, choose_KF, choose_SF, Confirm
import FuncLibrary

database = sqlite3.connect("ItemFiles.db")
table = "briefing"
tableschema = "user_id, mo, di, mi, do , fr, sa, so"
week = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
cs = database.cursor()


class BriefingSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="briefing")
    async def briefing(self, ctx: Context):

        # es wärde hie lääri values iiträge, damit die später chöi gänderet wärde.
        # ig due t database hie scho committe, dass we ä fähler passiert, dass ses när nid problem git.

        chosen = []
        choicebtns = ChooseWeekdays(ctx=ctx, mo=False, di=False, mi=False, do=False, fr=False, sa=False, so=False)
        choice = await ctx.reply("An welchen Tagen möchtest du ene Nachricht erhalten? ", view=choicebtns)

        while not choicebtns.confirm:
            await choicebtns.wait()

            if not choicebtns.confirm:
                chosen.append(choicebtns.choice)

                choicebtns = ChooseWeekdays(ctx=ctx,
                                            mo="mo" in chosen, # die wo si drückt worde wärde disabled
                                            di="di" in chosen,
                                            mi="mi" in chosen,
                                            do="do" in chosen,
                                            fr="fr" in chosen,
                                            sa="sa" in chosen,
                                            so="so" in chosen)

            await choice.edit(view=choicebtns) # die nöie buttons wärde inebracht wöu die aute nümme bruchbar si.
        chosen.sort(key=lambda m:week.index(m.capitalize()))

        cs.execute("DELETE FROM briefing WHERE user_id = ?", (int(ctx.author.id),))
        cs.execute("INSERT INTO briefing VALUES (?, '', '', '', '', '', '', '', 'all', 'all', 'all', 'all')",
                   (int(ctx.author.id),))

        for i in chosen:
            choiceforday= []
            button = ChooseTime(ctx, [])

            while not button.confirm:
                button = ChooseTime(ctx, choiceforday)

                await choice.edit(content=f"Bitte gib die Zeiten an für:\n\t{i.capitalize()}", view=button)
                await button.wait()

                if not button.confirm:
                    choiceforday.append(button.choice)

            cs.execute(f"UPDATE briefing SET {i}=? WHERE user_id = {ctx.author.id}", (str(choiceforday), ))

        button = choose_SF(ctx)
        await choice.edit(content="Was ist dein SF?", view=button)
        await button.wait()
        sf = button.sf

        button = choose_EF(ctx)
        await choice.edit(content="Was ist dein EF?", view=button)
        await button.wait()
        ef = button.ef

        button = choose_KF(ctx)
        await choice.edit(content="Was ist dein SF?", view=button)
        await button.wait()
        kf = button.kf

        button = Confirm(ctx)
        await choice.edit(content="Hast du MINT?", view=button)
        await button.wait()
        if button.confirm:
            mint = "MINT"
        else:
            mint="all"

        cs.execute(f"UPDATE briefing SET sf=?, ef=?, kf=?, mint=? WHERE user_id = {ctx.author.id}", (sf, ef, kf, mint))
        database.commit()

        await choice.edit(content="Wurde eingetragen", view=None)

    @commands.command(name="settings")
    async def settings(self, ctx:Context):
        settingsoutput = nextcord.Embed(title="Einstellungen")
        settings = cs.execute("SELECT  mo, di, mi, do, fr, sa, so FROM briefing WHERE user_id=?", (ctx.author.id,)).fetchall()[0]
        for i in range(len(settings)):
            if settings[i]:
                zeiten=settings[i][1:-1].replace(",", "\n").replace("'", "")
                settingsoutput.add_field(name=FuncLibrary.weekdays[i], value=zeiten)

        settingsoutput.set_footer(text="Du kannst die Einstellungen mit !briefing neu setzen")
        await ctx.channel.send(embed=settingsoutput)


def setup(client):
    client.add_cog(BriefingSetup(client))
