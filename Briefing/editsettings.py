import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import Buttons
import sqlite3

database = sqlite3.connect("ItemFiles.db", timeout=10)
cs = database.cursor()

weekdays = ["mo", "di", "mi", "do", "fr", "sa", "so"]


async def editdates(ctx:Context):
    chosen = []

    olddates = cs.execute("SELECT mo, di, mi, do, fr, sa, so FROM briefing WHERE user_id = ?", (ctx.author.id,)).fetchall()

    if olddates:
        for i in range(len(olddates[0])):
            if olddates[0][i]:
                chosen.append(weekdays[i])

    else:
        cs.execute(f"INSERT INTO briefing VALUES ({ctx.author.id}, '','','','','','','','','','','')")
    oldchoice = [i for i in chosen]

    choicebtns = Buttons.ChooseWeekdays(ctx=ctx)

    for child in choicebtns.children:
        if child.label.lower() in chosen:
            child.style = nextcord.ButtonStyle.grey

    editor_message = await ctx.reply("An welchen Tagen möchtest du ene Nachricht erhalten? ", view=choicebtns)

    while not choicebtns.confirm:
        await choicebtns.wait()
        if not choicebtns.confirm:
            chosen.append(choicebtns.choice)
            choicebtns = Buttons.ChooseWeekdays(ctx=ctx)

            # Luegt öb ä button isch drückt worde. Wenn ja, denn wirder grau. Wener aber 2mau isch drückt worde,
            # de wächsleter d buttonfarb zu blau.

            for button in choicebtns.children:
                if button.label.lower() in chosen:
                    if chosen.count(button.label.lower()) > 1:

                        chosen[:] = [a for a in chosen if a != button.label.lower()]

                        button.style = nextcord.ButtonStyle.blurple

                    else:
                        button.style = nextcord.ButtonStyle.grey

        await editor_message.edit(view=choicebtns)

    chosen.sort(key = lambda day:weekdays.index(day))

    for i in oldchoice:
        if not i in chosen:
            cs.execute(f"UPDATE briefing SET {i}=? WHERE user_id = {ctx.author.id}", ("",))
            database.commit()

    for i in chosen:
        if olddates:
            choiceforday = cs.execute(f"SELECT {i} FROM briefing WHERE user_id=?",
                                      (ctx.author.id,)).fetchall()[0][0][1:-1].replace("'", "").replace(" ", "").split(",")

            if not choiceforday[0]:
                choiceforday = []
                # we für dä tag nüt iigspicheret isch, de isch d iste läär. schüsch het me problem
                # dass me när e liste ["", 7:00, 9:00, usw.]  het.

        else:
            choiceforday = []

        button = Buttons.ChooseTime(ctx)

        while not button.confirm:
            button = Buttons.ChooseTime(ctx)

            for child in button.children:
                if child.label in choiceforday:
                    if choiceforday.count(child.label) > 1:

                        choiceforday[:] = [x for x in choiceforday if x != child.label and x]

                        child.style = nextcord.ButtonStyle.blurple

                    else:
                        child.style = nextcord.ButtonStyle.grey

            await editor_message.edit(content=f"Bitte gib die Zeiten an für:\n\t{i.capitalize()}", view=button)
            await button.wait()

            if not button.confirm and button.choice:
                choiceforday.append(button.choice)

        choiceforday.sort(key=lambda time:int(time.split(":")[0]))

        cs.execute(f"UPDATE briefing SET {i}=? WHERE user_id = {ctx.author.id}", (str(choiceforday),))
        database.commit()

    await editor_message.edit(content="Änderungen wurden vorgenommen", view=None, delete_after=20)


async def edit_classes(ctx:Context):
    previouschoices = cs.execute(f"SELECT sf, ef, kf FROM briefing WHERE user_id = {ctx.author.id}").fetchall()
    button = Buttons.choose_SF(ctx)
    if previouschoices:
        for child in button.children:
            if child.label == previouschoices[0][0][3::]:
                child.style = nextcord.ButtonStyle.green

    editor = await ctx.reply(content="Was ist dein SF?", view=button)

    await button.wait()
    sf = button.sf

    button = Buttons.choose_EF(ctx)
    if previouschoices:
        for child in button.children:
            if child.label == previouschoices[0][1][3::]:
                child.style = nextcord.ButtonStyle.green

    await editor.edit(content="Was ist dein EF?", view=button)

    await button.wait()
    ef = button.ef

    button = Buttons.choose_KF(ctx)
    if previouschoices:
        for child in button.children:
            if child.label == previouschoices[0][2][3::]:
                child.style = nextcord.ButtonStyle.green

    await editor.edit(content="Was ist dein KF?", view=button)
    await button.wait()
    kf = button.kf

    button = Buttons.Confirm(ctx)

    await editor.edit(content="Hast du MINT?", view=button)
    await button.wait()
    if button.confirm:
        mint = "MINT"
    else:
        mint = "all"

    cs.execute(f"UPDATE briefing SET sf=?, ef=?, kf=?, mint=? WHERE user_id = {ctx.author.id}", (sf, ef, kf, mint))
    database.commit()

    await editor.edit(content="Wurde eingetragen", view=None, delete_after=20)

