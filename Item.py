import datetime
import encoding
import sqlite3
Itemfile = "ItemFiles.db"
Alltables = "testitems", "items"
Itemtable = "testitems"
tablecategories = ("datum", "kagegorie", "fach", "aufgabe")

weekdays = ["Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",
            "Sonntag"]  # es git vor datetime-library ä command wo tuet dr wuchetag vomne datum zrüggäh,
                        # allerdings nur aus integer. Ds isch für ds formatting.


def changefachname(fach):  # so isches übersichtlecher
    if fach == "Französisch":
        fach = "Franz"
    elif fach == 'Englisch':
        fach = 'English'
    elif fach == 'Biologie':
        fach = 'Bio'
    elif fach == 'Geschichte':
        fach = 'History'

    return fach


def newItem(category, database):
    error = 1
    while error == 1:
        try:
            dateraw = input("Wann ist der Test oder die Aufgabe fällig? ")
            date = str(datetime.date(int(dateraw.split(".")[2]),
                                     int(dateraw.split(".")[1]),
                                     int(dateraw.split(".")[0])))
            # datetime.date nimmt daten nur in der Form YY/MM/DD an
            error = 0

        except:
            print("ungültiges Datum")
            continue
            # fragt nachemne valid input bis ä valid input gäh wird.

    fach = changefachname(input("Welches Fach? ").capitalize())


    if category == "Hausaufgabe":
        aufgabe = input("Aufgabe: ")

    elif input("Schon Lernziele? ").lower != "ja":
        aufgabe = None

    else:
        aufgabe = input("Lernziele: ")

    database.cursor().execute(f"INSERT INTO {Itemtable} VALUES ('{date}', '{category}', '{fach}', '{aufgabe}')")
    database.commit()


def searchItems(search=None):
    results = []
    items = encoding.getallitems()

    if search == "":
        results = items

    else:
        for keyword in search.split(" "):
            for item in items:
                keyword = changefachname(keyword.capitalize())  # mues für input und output ou so si
                if keyword.lower().capitalize() in item and item not in results:
                    results.append(item)

    if results == []:
        output =  "Keine resultate gefunden"

    else:
        output = ""
        for i in results:
            output += layout(i)

    return output


def layout(item):
    (year, month, day) = item[0].split("-")

    return f"\n{str(weekdays[datetime.date(int(year), int(month), int(day)).weekday()])}, {day}.{month}.{year}\n" \
           f"{item[1].capitalize()} {item[2]}" \
           f"\n{item[3]}\n"

    # ersti zile git wuchetag sowie datum zrügg.
    # die 2ti git kategorie und fach zrügg (kategorie isch entweder "Test" oder "Hausaufgabe")
    # die 3tti git d ufgab zrügg (oder d lernziu weses ä tescht isch)

    # wägem formatting isches so, dass d datebank d ä output aus liste zrüggbringt.
    # aso wemer üs d datebank aus tabäue vorsteue, de git üs d datebank für nes bestimmts item fougendes use:
    #   [{spaute 1}, {spaute 2}, {spaute 3}...]

    # I üsem fau isch das:
    #   [Itemid, datum, kategorie, fach, ufgab].

