import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import sqlite3
from Buttons import ChooseDatum
from datetime import datetime, timedelta, date


async def add_birthday(client:nextcord.Client, ctx:Context) -> None:
    db = sqlite3.connect("ItemFiles.db")
    cs = db.cursor()

    # in loop cuz if the day is above 25, then the program has to recreate the view-object
    # so if you choose "above 25", then the view will reset,
    # but the day-dropdown will show the choices above 25, as well as an option to go back down.
    bounds = (2003, 2006)
    msg_view = ChooseDatum(ctx, year_bounds=bounds)
    msg = await ctx.channel.send("Wann ist dein Geburtstag?", view=msg_view)
    while not msg_view.over:
        if msg_view.exit:
            break
        else:
            msg_view = ChooseDatum(ctx, day=msg_view.day, month=msg_view.month,
                                   year=msg_view.year, year_bounds=bounds)
            await msg.edit(view=msg_view)
            await msg_view.wait()

    # cleanup
    await msg.delete()
    await ctx.message.add_reaction("✅")

    # If the user did not break, then he is added to the table, as well as his next birthday
    if not msg_view.exit:
        # if the user has already an entry (f.e. he turned the notifications of),
        # then their instance in the db gets deleted and then re-added.
        if cs.execute(f"SELECT * FROM birthdays WHERE id={ctx.author.id}").fetchone():
            cs.execute(f"DELETE FROM birthdays WHERE id={ctx.author.id}")

        # the birthday of the user is added to the db
        cs.execute(f"INSERT INTO birthdays VALUES ({ctx.author.id}, {int(msg_view.day)}, {int(msg_view.month)}, "
                   f"{int(msg_view.year)}, true)")

        db.commit()
        # their subsequent birthday gets added as well
        now = (datetime.utcnow() + timedelta(hours=2)).date()
        b_date = date(now.year, msg_view.month, msg_view.day)
        if now > b_date:
            b_date.replace(year=b_date.year+1)

        fach = client.get_channel(912264818516430849).name

bugfix (shoul)        cs.execute(f"INSERT INTO items VALUES ({str(b_date)}, '', ?, ?, 'all')",
                   (fach, f'Geburtstag {ctx.author.name}'))
        db.commit()
        db.close()


def notification_off(userid:int):
    db = sqlite3.connect("ItemFiles.db")
    cs = db.cursor()
    cs.execute(f"INSERT INTO birthdays VALUES ({userid}, 0, 0, 0, false)")
    db.commit()
    db.close()


def notifs(userid:int) -> str:
    db = sqlite3.connect("ItemFiles.db")
    cs = db.cursor()
    if not cs.execute(f"SELECT * FROM birthdays WHERE id = {userid}").fetchone():
        return "**Tipp**: gib '!birthday' ein, um deinen Geburtstag einzutragen\n" \
               "*(du kannst diese notification mit '!end_notifs' abstellen.*"
    else:
        return ""