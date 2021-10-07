import datetime
import encoding

weekdays = ["Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",
            "Sonntag"]  # es git vor datetime-library ä command wo tuet dr wuchetag vomne datum zrüggäh, allerdings nur aus integer. Ds isch für ds formatting



def newItem(category):
    error = 1
    while error == 1:
        try:
            dateraw = input("Wann? ")
            date = str(datetime.date(int(dateraw.split(".")[2]),
                                     int(dateraw.split(".")[1]),
                                     int(dateraw.split(".")[0])))
            # datetime.date nimmt daten nur in der Form YY/MM/DD an
            error = 0

        except:
            print("ungültiges Datum")
            continue

    fach = input("Welches Fach? ").lower().capitalize()
    if fach == "Französisch":
        fach = "Franz"

    if category == "Hausaufgabe":
        aufgabe = input("Aufgabe: ")

    elif input("Schon Lernziele? ").lower != "ja":
        aufgabe = None
    else:
        aufgabe = input("Lernziele: ")

    encoding.newitem(datum=date, kategorie=category, fach=fach, aufgabe=aufgabe)

def searchItems(search=None):
    results = []
    itemcounter = 0 #Mit jedem ausgedruckten Item wird es 1 grösser. Wenn am ende der counter==0, dann hat das programm nihts gefunden

    items = encoding.getallitems()
    if search == "":
        results = items
    else:
        for keyword in search.split(" "):
            for item in items:
                if keyword.lower().capitalize() in item:
                    results.append(item)
                    itemcounter +=1

    if results == []:
        yield "keine resultate gefunden"

    else:
        for item in results:
            (year, month, day) = item[1].split("-")


            yield f"{str(weekdays[datetime.date(int(year), int(month), int(day)).weekday()])}, {day}.{month}.{year}\n" \
                  f"{item[2].capitalize()} {item[3]}" \
                  f"\n{item[4]}\n"

            # ersti zile git wuchetag sowie datum zrügg.
            # die 2ti git kategorie und fach zrügg (kategorie isch entweder "Test" oder "Hausaufgabe")
            # die 3tti git d ufgab zrügg (oder d lernziu weses ä tescht isch)

            # wägem formatting isches so, dass d datebank d ä output aus liste zrüggbringt.
            # aso wemer üs d datebank aus tabäue vorsteue, de git üs d datebank für nes bestimmts item fougendes use:
            #   [{spaute 1}, {spaute 2}, {spaute 3}...]

            # I üsem fau isch das:
            #   [Itemid, datum, kategorie, fach, ufgab].

            # Darum bruchi ou kei "i[0]", wöu für das isch d Itemid irrelevant. d ID wäri dänkt für kommunikation innerhaub vom programm.





