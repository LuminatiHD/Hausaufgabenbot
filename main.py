# TODO:
#  - Tests und HA editieren können
#  - Sortieren nach:
#       - Datum
#       - Fach
#       - Lernziele
#  - nach bald kommenden Aufgaben und Tests abfragen können (
#  - Reminders vor Tests
#  - Private Aufgaben eintragen und individuell ausgeben können
#    (also für Gruppenarbeiten, EF-arbeiten, ind. Vorträge etc.)
#  - Stundenplan ausgeben können (auch nach indiv. Anpassung)
#  - Wenn jemand zu einem Test eine Zusammenfassung oder ein Quizlet oder so macht, dann kann man die Nachricht beim Bot eintragen
#  - Better Design with Colors
#  - option to delete things on request


# IDEAS:
#   -man könnte den Stundenplan mit Buttons konstruieren
#   und wenn man die Knöpfe drückt, dann werden alle kommenden Items für das Fach angezeigt


"""
wieme cha gseh isch ds momentane programm no nid mit discord integriert. Ds isch eifach mau wieme ds mitem datehandling macht.
fürs programm würdi euch empfähle, euch usenang ds setzte, wie me d sqlite3-library bruucht (me mues se nid separat installiere)
"""

import datetime
import json
import Item
from Item import newItem, searchItems
import sqlite3
import nextcord
from nextcord.ext import commands, tasks


Itemfile = "ItemFiles.db"
Alltables = "testitems", "items"
Itemtable = "testitems"
tablecategories = ("datum", "kagegorie", "fach", "aufgabe")
database = sqlite3.connect(Itemfile)

def options():
    inp = input(f' Was möchtest du machen? \n A: Neue Aufgabe \n B: Neuer Test \n C: outlook \n\n')
    if inp.lower() == 'neue aufgabe' or inp.lower() == 'a':
        print('Hausaufgabe')
        newItem("Hausaufgabe", database)


    elif inp.lower() == "neuer test" or inp.lower() == 'b':
        print('Test')
        newItem("Test", database)


    elif inp.lower().startswith("outlook") or inp.lower() == 'c':
        print(searchItems(database, search=inp[8:]))


    elif inp.lower() == "wipe": # leert die Tabelle (braucht noch weitere bestätigung, wird in encoding gehandlet)
        database.cursor().execute(f"DELETE FROM {Itemtable}")

    elif inp.lower() == "exit":
        database.close()
        exit()

    else:
        print("Befehl nicht erkannt")

    # ufgabe oder teschts wo scho düre si wärde glöschet
    allitems = database.cursor().execute(f"SELECT datum, rowid FROM {Itemtable} ORDER BY datum").fetchall()

    for item in allitems:
        if str(datetime.date.today()) > item[0]:
            database.cursor().execute(f"DELETE FROM {Itemtable} WHERE rowid = {item[1]}")


while True:
    print("=============================")
    options()
    database.commit()

