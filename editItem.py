import Buttons
import sqlite3
import datetime
Itemfile = "ItemFiles.db"
Alltables = "testitems", "items"
Itemtable = "items"
tablecategories = ("datum", "kategorie", "fach", "aufgabe", "access")
database = sqlite3.connect(Itemfile)
Itemkategorien = ("Test", "Aufgabe")


def changefachname(fach):  # so isches übersichtlecher
    fach = fach.capitalize()
    if fach == "Französisch":
        fach = "Franz"
    elif fach == 'Englisch':
        fach = 'English'
    elif fach == 'Biologie':
        fach = 'Bio'
    elif fach == 'Geschichte':
        fach = 'History'

    return fach


async def editItem(self, ctx, selecteditem):
    editor = await ctx.reply("Was genau möchtest du editieren?")
    editorbtn = Buttons.EditButtons(ctx)
    await editor.edit(view=editorbtn)
    await editorbtn.wait()
    if "kategorie" in editorbtn.edit:
        confirm = Buttons.Confirm(ctx)
        while not confirm.confirm:
            confirm = Buttons.Confirm(ctx)
            newcategorychoice = Buttons.TestOrHA(ctx)
            category = selecteditem[1]

            await editor.edit(content="Neue Kategorie: ", view=newcategorychoice)
            await newcategorychoice.wait()
            newcategory = newcategorychoice.choice
            if not category:
                category = "Unspezifisch"
            await editor.edit(
                content=f"Alte Kategorie: {category}\nNeue Kategorie: {newcategory if newcategory else 'Unpezifisch'}\nBestätigen?",
                view=confirm)
            await confirm.wait()

        if confirm.confirm:
            database.cursor().execute(
                f"UPDATE {Itemtable} SET kategorie = '{newcategory}'WHERE rowid = {selecteditem[5]}")

    if "aufgabe" in editorbtn.edit:
        confirm = Buttons.Confirm(ctx)
        while not confirm.confirm:
            confirm = Buttons.Confirm(ctx)
            await ctx.reply("Aufgabe: ")
            newaufg = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)
            await newaufg.reply(f"Alte Aufgabe: {selecteditem[3]}\nNeue Aufgabe: {newaufg.content}.\nBestätigen?",
                                view=confirm)
            await confirm.wait()
        database.cursor().execute(
            f"UPDATE {Itemtable} SET aufgabe = '{newaufg.content}' WHERE rowid = {selecteditem[5]}")

    if "datum" in editorbtn.edit:
        error = True
        confirm = Buttons.Confirm(ctx)
        while error and not confirm.confirm:
            confirm = Buttons.Confirm(ctx)
            await ctx.message.reply("Wann ist der Test oder die Aufgabe fällig?")
            try:
                dateraw = await self.bot.wait_for("message",
                                                  check=lambda msg: msg.author == ctx.author)
                datum = str(datetime.date(int(dateraw.content.split(".")[2]),
                                          int(dateraw.content.split(".")[1]),
                                          int(dateraw.content.split(".")[0])))

                await dateraw.reply(f"Altes Datum: {selecteditem[0]}\nNeues Datum: {datum}\nBestätigen?", view=confirm)
                await confirm.wait()
                error = False
            except:
                await ctx.reply("ungültiges Datum")
                continue
        database.cursor().execute(f"UPDATE {Itemtable} SET datum = '{datum}' WHERE rowid = {selecteditem[5]}")
    if "fach" in editorbtn.edit:
        confirm = Buttons.Confirm(ctx)
        while not confirm.confirm:
            confirm = Buttons.Confirm(ctx)
            await ctx.reply("Fach: ")
            newfach = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)

            await newfach.reply(f"Altes Fach: {selecteditem[2]}\nNeues Fach: "
                                f"{changefachname(newfach.content)}.\nBestätigen?", view=confirm)
            await confirm.wait()
        database.cursor().execute(
            f"UPDATE {Itemtable} SET fach = '{changefachname(newfach.content)}' WHERE rowid = {selecteditem[5]}")

    if "access" in editorbtn.edit:
        confirm = Buttons.Confirm(ctx)
        while not confirm.confirm:
            newacc = Buttons.ManageItemAccess(ctx)
            confirm = Buttons.Confirm(ctx)
            await editor.edit(content="Zugriff: ", view=newacc)
            await newacc.wait()
            oldaccess = selecteditem[4]
            if selecteditem[4].isnumeric():
                oldaccess = "private"
            await editor.edit(f"Alter Zugriff: {oldaccess}\nNeuer Zugriff: "
                               f"{newacc.access}.\nBestätigen?", view=confirm)
            await confirm.wait()
            access = newacc.access
            if newacc.access == "private":
                access = ctx.author.id
        database.cursor().execute(
            f"UPDATE {Itemtable} SET access = '{access}' WHERE rowid = {selecteditem[5]}")
    if not editorbtn.goback:  # weme dr "Zurück"-button drückt de isch goback=True
        database.commit()
        await ctx.channel.send("Änderungen wurden vorgenommen")
    else:
        await ctx.channel.send("Editng-mode wird verlassen")