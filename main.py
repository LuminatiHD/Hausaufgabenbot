# TODO:
#  - Tests und HA editieren können
#  - Sortieren nach:
#       - Datum
#       - Fach
#       - Lernziele
#  - nach bald kommenden Augaben und Tests abfragen können (
#  - Reminders vor Tests
#  - Private Aufgaben eintragen und individuell ausgeben können
#    (also für Gruppenarbeiten, EF-arbeiten, ind. Vorträge etc.)
#  - Stundenplan ausgeben können (auch nach indiv. Anpassung)
#  - Wenn jemand zu einem Test eine Zusammenfassung oder ein Quizlet oder so macht, dann kann man die Nachricht beim Bot eintragen
#  - Better Design with Colors


# IDEAS:
#   -man könnte den Stundenplan mit Buttons konstruieren
#   und wenn man die Knöpfe drückt, dann werden alle kommenden Items für das Fach angezeigt


"""
wieme cha gseh isch ds momentane programm no nid mit discord integriert. Ds isch eifach mau wieme ds mitem datehandling macht.
fürs programm würdi euch empfähle, euch usenang ds setzte, wie me d sqlite3-library bruucht (me mues se nid separat installiere)
"""



import datetime
import json
from Item import newItem, searchItems
import encoding


def datesort(elem):
    return elem["Datum"]  # wird nur gebraucht für das sortieren der Liste nach Datum

tablecategories = ("id", "datum", "kagegorie", "fach", "aufgabe")

while True:
    inp = input("Input: ")
    if inp.lower() == "neue aufgabe":
        newItem("Hausaufgabe")

    if inp.lower() == "neuer test":
        newItem("Test")

    if inp.lower().startswith("outlook"):
        for i in searchItems(search=inp[8:]):
            print(i)

    else:
        print("Befehl nicht erkannt")
    allitems = encoding.getallitems()

    for item in allitems:
        (year, month, day) = item[1].split("-")
        if datetime.date.today() > datetime.date(int(year), int(month), int(day)):
            encoding.deleteitem(item[0])

            #ufgabe oder teschts wo scho düre si wärde glöschet
