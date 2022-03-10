import Buttons
import sqlite3
import datetime
import FuncLibrary

Itemfile = "ItemFiles.db"
Alltables = "testitems", "items"
Itemtable = "items"
tablecategories = ("datum", "kategorie", "fach", "aufgabe", "access")

database = sqlite3.connect(Itemfile, timeout=10)
Itemkategorien = ("Test", "Aufgabe")


async def editItem(self, ctx, selecteditem, editor):
    await editor.edit("Was genau möchtest du editieren?")

    editorbtn = Buttons.Dropdown_Menu(ctx, [i.capitalize() for i in tablecategories], min=1, max=len(tablecategories))
    await editor.edit(view=editorbtn)
    await editorbtn.wait()

    for i in editorbtn.children:
        i.disabled = True

    await editor.edit(view=editorbtn)
    await editorbtn.wait()
# ============================================== KATEGORIE ==============================================
    if "Kategorie" in editorbtn.output:
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
                content=f"Alte Kategorie: {category}"
                        f"\nNeue Kategorie: {newcategory if newcategory else 'Unpezifisch'}"
                        f"\nBestätigen?",
                view=confirm)
            await confirm.wait()

        if confirm.confirm:
            database.cursor().execute(
                f"UPDATE {Itemtable} SET kategorie = ? WHERE rowid = ?",
                (newcategory, selecteditem[5]))
            database.commit()

# ============================================== ACCESS ==============================================
    if "Access" in editorbtn.output:
        confirm = Buttons.Confirm(ctx)
        while not confirm.confirm:
            newacc = Buttons.ManageItemAccess(ctx)
            confirm = Buttons.Confirm(
                ctx)  # ig tue dr button neu generiere wöu schüsch chasch dr button nümme drücke
            # de funktioniert z confirme nid.
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
            f"UPDATE {Itemtable} SET access = '{access}' WHERE rowid = ?", (selecteditem[5],))
        database.commit()

# ============================================== DATUM ==============================================
    if "Datum" in editorbtn.output:
        confirm = Buttons.Confirm(ctx)

        while not confirm.confirm:

            confirm = Buttons.Confirm(ctx)

            menu = Buttons.ChooseDatum(ctx)
            await editor.edit("Wann ist der Test oder die Aufgabe fällig?", view=menu)

            while not menu.over:
                menu = Buttons.ChooseDatum(ctx, menu.day, menu.month, menu.year)
                await editor.edit(view=menu)
                await menu.wait()
                if menu.exit:
                    break

            if menu.exit:
                break

            for i in menu.children:
                i.disabled = True

            await editor.edit(view=menu)

            datum = datetime.date(int(menu.year), int(menu.month), int(menu.day))

            olddatum = datetime.date(int(selecteditem[0].split("-")[0]),

                                     int(selecteditem[0].split("-")[1]),

                                     int(selecteditem[0].split("-")[2]))

            await editor.edit(content=f"Altes Datum: {olddatum.day}.{olddatum.month}.{olddatum.year}"

                                         f"\nNeues Datum: {datum.day}.{datum.month}.{datum.year}\nBestätigen?",
                                         view=confirm)

            await confirm.wait()

        if not menu.exit:
            database.cursor().execute(f"UPDATE {Itemtable} SET datum = ? WHERE rowid = ?",
                                      (str(datum), selecteditem[5]))
            database.commit()

# ============================================== AUFGABE ==============================================
    if "Aufgabe" in editorbtn.output:
        confirm = Buttons.Confirm(ctx)
        while not confirm.confirm:
            confirm = Buttons.Confirm(ctx)
            askmsg = await ctx.reply("Aufgabe: ")
            newaufg = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)

            await askmsg.delete()
            confirmmsg = await newaufg.reply(f"Alte Aufgabe: {selecteditem[3]}\nNeue Aufgabe: {newaufg.content}\nBestätigen?",
                                view=confirm)
            await confirm.wait()
            await confirmmsg.delete()
        database.cursor().execute(
            f"UPDATE {Itemtable} SET aufgabe = ? WHERE rowid = ?",
            (newaufg.content, selecteditem[5]))
        database.commit()

# ============================================== DATUM ==============================================
    elif "datum" in editorbtn.edit:
        confirm = Buttons.Confirm(ctx)

        while not confirm.confirm:

            confirm = Buttons.Confirm(ctx)

            menu = Buttons.ChooseDatum(ctx)
            await editor.edit("Wann ist der Test oder die Aufgabe fällig?", view=menu)

            while not menu.over:
                menu = Buttons.ChooseDatum(ctx, menu.day, menu.month, menu.year)
                await editor.edit(view=menu)
                await menu.wait()
                if menu.exit:
                    break

            if menu.exit:
                break

            for i in menu.children:
                i.disabled = True

            await editor.edit(view=menu)

            datum = datetime.date(int(menu.year), int(menu.month), int(menu.day))

            olddatum = datetime.date(int(selecteditem[0].split("-")[0]),

                                     int(selecteditem[0].split("-")[1]),

                                     int(selecteditem[0].split("-")[2]))

            confirmmsg = await ctx.reply(f"Altes Datum: {olddatum.day}.{olddatum.month}.{olddatum.year}"
        
                                         f"\nNeues Datum: {datum.day}.{datum.month}.{datum.year}\nBestätigen?", view=confirm)

            await confirm.wait()
            await confirmmsg.delete()

        if not menu.exit:
            database.cursor().execute(f"UPDATE {Itemtable} SET datum = ? WHERE rowid = ?",
                                      (str(datum), selecteditem[5]))
            database.commit()

# ============================================== FACH ==============================================
    if "Fach" in editorbtn.output:
        confirm = Buttons.Confirm(ctx)
        while not confirm.confirm:
            confirm = Buttons.Confirm(ctx)
            askmsg = await ctx.reply("Fach: ")
            newfach = await self.bot.wait_for("message", check=lambda msg: msg.author == ctx.author)

            await askmsg.delete()
            confirmmsg = await newfach.reply(f"Altes Fach: {selecteditem[2]}\nNeues Fach: "
                                f"{FuncLibrary.changefachname(newfach.content)}.\nBestätigen?", view=confirm)
            await confirm.wait()
            await confirmmsg.delete()

        database.cursor().execute(
            f"UPDATE {Itemtable} SET fach = ? WHERE rowid = ?",
            (FuncLibrary.changefachname(newfach.content), selecteditem[5]))
        database.commit()

# ============================================== CLEANUP ==============================================
    if not editorbtn.goback:  # weme dr "Zurück"-button drückt de isch goback=True
        database.commit()
        await ctx.channel.send("Gegebene Änderungen wurden vorgenommen")
    else:
        await ctx.channel.send("Editng-mode wird verlassen")
    await editor.delete()