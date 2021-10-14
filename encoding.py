import sqlite3
Itemfile = "ItemFiles.db"
Alltables = "testitems", "items"
Itemtable = "testitems"
tablecategories = ("datum", "kagegorie", "fach", "aufgabe")

"""
Hie wird aues punkto kommunikation zur datebank ghandlet. Wie genau me ds mues mitder datebank mache weisi no nid. 
Weder d datebank nid heit downloadet, müesst dir zersch die commands usfüere:
    file = sqlite3.connect("ItemFiles.db") 
    file.cursor().ececute("CREATE TABLE testitems (id INTEGER, datum TEXT, fach TEXT, aufgabe TEXT)

des tuet d tabäue ersteue, mit welem ds programm interagiert

weder weit, chame d datebank wie vougt lösche:
    file = sqlite3.connect("ItemFiles.db") 
    file.cursor().execute("DROP TABLE testitems)

de müesster eifach när die tabäue wider neu kreiere.
"""


def getallitems():
    file = sqlite3.connect(Itemfile)
    return file.cursor().execute(f"SELECT *, rowid FROM {Itemtable}").fetchall()


def newitem(datum, kategorie, fach, aufgabe):
    file = sqlite3.connect(Itemfile)
    file.cursor().execute(f"INSERT INTO {Itemtable} VALUES ('{datum}', '{kategorie}', '{fach}', '{aufgabe}')")
    file.commit()

def edititem(kategorie, new, itemid):
    file = sqlite3.connect(Itemfile)
    file.cursor().execute(f"UPDATE {Itemtable} SET {kategorie} = '{new}' WHERE rowid = '{itemid}'")
    file.commit()

def deleteitem(id):
    file = sqlite3.connect(Itemfile)
    file.cursor().execute(f"DELETE FROM {Itemtable} WHERE rowid = {id}")
    file.commit()

def wipetable():
    if input(f"Wollen Sie wirklich die Tabelle {Itemtable} leeren? ").lower() == "ja":
        file = sqlite3.connect(Itemfile)
        for elem in file.cursor().execute(f"SELECT rowid FROM {Itemtable}").fetchall():
            deleteitem(elem[0])
        file.commit()
# tuet d tabäue {Itemtable} lääre (meh d tabäue lösche und neu ersteue, isch ds gliiche basically