import nextcord
from datetime import timedelta, date, datetime
import sqlite3
Itemfile = "ItemFiles.db"
database = sqlite3.connect(Itemfile)
cs = database.cursor()


weekdays = ["Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",  # es git vor datetime-library ä command wo tuet dr wuchetag vomne datum zrüggäh,
            "Sonntag"]  # allerdings nur aus integer. Ds isch für ds formatting.

StP_colors = {"deutsch":0xffdd00,
              "geschichte":0xcc8904,
              "englisch":0xff0011,
              "math":0x097dd6,
              "franz":0x09a6d6,
              "physik":0x2847ad,
              "bio":0x0eab25,
              "chemie":0x48fac2,
              "sport":0x821705,
              "mint":0xe1e2eb,
              "musik":0x1bd18e,
              "bg":0x9f11c2,
              "sf physik": 0x041859,
              "sf am": 0x5e0303,
              "sf Bio":0x06701d,
              "sf Chemie":0x08d134,
              "sf Wirtschaft": 0xe01094,
              "sf Recht": 0xe010cf,
              "sf pp":0xf72fc9,
              "ef musik":0xdbce14,
              "ef geschichte":0xa85507,
              "ef info":0x10e0c5,
              "ef pp":0xe0103a,
              "ef philo":0xb80b6a,

             }


def get_access_permissions(author):
    try:
        ef = "all"
        sf = "all"
        kf = "all"
        mint = "all"
        for role in author.roles:
            if role.name.lower().startswith("ef"):
                ef = role.name
            elif role.name.lower().startswith("sf"):
                sf = role.name
            elif role.name.lower().startswith("kf"):
                kf = role.name
            elif role.name.lower().startswith("mint"):
                mint = role.name

    except AttributeError:  # für DM-modus
        perm = cs.execute(f"SELECT sf, ef, kf, mint FROm briefing WHERE user_id = {author.id}").fetchall()
        if perm:
            sf = perm[0][0]
            ef = perm[0][1]
            kf = perm[0][2]
            mint = perm[0][3]
        else:
            sf = "all"
            ef = "all"
            kf = "all"
            mint = "all"
    return sf, ef, kf, mint


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


def layout(items, footer):
    i = 1
    today = False
    tmrw = False
    week_1 = False
    week_2 = False
    month_1 = False
    month_2 = False
    future = False
    output = nextcord.Embed()
    for item in items:
        (year, month, day) = item[0].split("-")
        itemdate = date(int(year), int(month), int(day))

        if itemdate==date.today() and not today:
            zeit = date.today()
            output.add_field(name="__HEUTE:__",
                             value=f"(Bis zum {zeit.day}.{zeit.month}.{zeit.year})",
                             inline=False)
            today = True

        elif itemdate==date.today()+timedelta(1) and not tmrw:
            zeit = date.today()+timedelta(1)
            output.add_field(name="__MORGEN:__",
                             value=f"(Bis zum {zeit.day}.{zeit.month}.{zeit.year})",
                             inline=False)
            tmrw = True

        # week_1 teschtet öb ds scho isch vergäh worde, wenn nid de machter das häre
        elif date.today()+timedelta(1)< itemdate <= date.today() + timedelta(7) and not week_1:
            zeit = date.today() + timedelta(7)
            output.add_field(name="__\nBIS NÄCHSTE WOCHE:__",
                             value=f"(Bis zum {zeit.day}.{zeit.month}.{zeit.year})",
                             inline=False)
            week_1 = True

        elif date.today() + timedelta(7) <= itemdate <= date.today() + timedelta(14) and not week_2:
            zeit = date.today() + timedelta(14)
            output.add_field(name="__\nNÄCHSTE 2 WOCHEN:__",
                             value=f"(Bis zum {zeit.day}.{zeit.month}.{zeit.year})", inline=False)
            week_2 = True

        elif date.today() + timedelta(14) < itemdate <= date.today() + timedelta(30) and not month_1:
            zeit = date.today() + timedelta(30)
            output.add_field(name="__\nINNERHALB VON 30 TAGEN:__",
                             value=f"(Bis zum {zeit.day}.{zeit.month}.{zeit.year})", inline=False)
            month_1 = True

        elif date.today() + timedelta(30) < itemdate <= date.today() + timedelta(60) and not month_2:
            zeit = date.today() + timedelta(60)
            output.add_field(name="__\nINNERHALB VON 60 TAGEN:__",
                             value=f"(Bis zum {zeit.day}.{zeit.month}.{zeit.year})", inline=False)
            month_2 = True

        elif date.today() + timedelta(60) < itemdate and not future:
            lastitem = items[-1][0].split("-")
            output.add_field(name="__\nSPÄTER ALS 60 TAGE:__",
                             value=f"(Bis zum {date(int(lastitem[0]), int(lastitem[1]), int(lastitem[2]))})", inline=False)
            future = True

        desc = item[3]
        if not desc:  # Wenn man keine Lernziele angegeben hat, dann ist desc=None.
            desc = "Keine Lernziele"

        elif len(desc) > 30:
            desc = item[3][:30]+"..."  # wöu schüsch chasch du lernziele ha wo viu ds läng si.

        output.add_field(name=f"{i}: {item[1].capitalize()} {item[2]}",
                         value=f" {str(weekdays[itemdate.weekday()])}, "
                               f"{day}.{month}.{year}\n {desc}\n ",
                         inline=False)

        output.set_footer(text=footer)
        i+=1
    return output


def outputbriefing(user, ef, sf, kf, mint):
    output = nextcord.Embed(title=f"{weekdays[date.today().weekday()]}, "
                                  f"{date.today().day}.{date.today().month}.{str(date.today().year)[2:]} "
                                  f"({datetime.now().hour}:{datetime.now().minute:02})")

    timeset = date.today()+timedelta(days=7)
    items = cs.execute(f"SELECT * FROM items WHERE datum <= ? AND (access = 'all' " \
                                      f"OR access = ? OR access = ? " \
                                      f"OR access = ? OR access = ?) ORDER BY datum",
                                      (timeset, user.id, sf, ef, kf)).fetchall()

    output.add_field(name="AUFGABEN UND TESTS DIESE WOCHE:",
                     value=f"(Bis {timeset.day}.{timeset.month}.{timeset.year})", inline=False)

    if items:
        for item in items:
            desc = item[3]
            if not desc:  # Wenn man keine Lernziele angegeben hat, dann ist desc=None.
                desc = "Keine Lernziele"

            elif len(desc) > 20:
                desc = item[3][:20] + "..."  # wöu schüsch chasch du lernziele ha wo viu ds läng si.

            (year, month, day) = item[0].split("-")
            itemdate = date(int(year), int(month), int(day))
            output.add_field(name=f" {item[1].capitalize()} {item[2]}",
                             value=f" {str(weekdays[itemdate.weekday()])}, "
                                   f"{day}.{month}.{year}\n {desc}\n ",
                             inline=False)

    else:
        output.add_field(name="Es ist nichts zu tun", value="Du kannst mit !new etwas hinzufügen.", inline=False)

    currdate = (datetime.now()+timedelta(hours=24-17)).date()
    tag = currdate.weekday()
    wochentage = ["Mo", "Di", "Mi", "Do", "Fr"]

    if tag > 4:
        tag = (currdate + (timedelta(7) - timedelta(tag))).weekday() # tag wird ufe mänti gsetzt
        output.add_field(name=".", value="**DER STUNDENPLAN VON MONTAG:**")

    elif currdate == date.today():
        output.add_field(name=".", value="**DER STUNDENPLAN VON HEUTE:**")

    else:
        output.add_field(name=".", value="**DER STUNDENPLAN VON MORGEN**")

    allitems = cs.execute(f"SELECT fach, time, room FROM Stundenplan_23b WHERE weekday = ?" \
                          " AND (access='all' OR access = ? OR access = ? OR access = ? OR access=?)", \
                          (wochentage[tag], ef, sf, kf, mint)).fetchall()

    allitems.sort(key=lambda elem: elem[1])
    for i in allitems:
        output.add_field(name=i[0], value=f"{i[1]}\n{i[2]}", inline=False)
    return output
