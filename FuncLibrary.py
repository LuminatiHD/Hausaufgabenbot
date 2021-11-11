import nextcord
from datetime import timedelta, date

weekdays = ["Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",  # es git vor datetime-library ä command wo tuet dr wuchetag vomne datum zrüggäh,
            "Sonntag"]  # allerdings nur aus integer. Ds isch für ds formatting.


def get_access_permissions(author):
    try:
        ef = "all"
        sf = "all"
        kf = "all"
        for role in author.roles:
            if role.name.lower().startswith("ef"):
                ef = role.name
            elif role.name.lower().startswith("sf"):
                sf = role.name
            elif role.name.lower().startswith("kf"):
                kf = role.name

    except AttributeError:  # für DM-modus
        sf = "all"
        ef = "all"
        kf = "all"
    return sf, ef, kf


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
    week_1 = False
    week_2 = False
    month_1 = False
    month_2 = False
    future = False
    output = nextcord.Embed()
    for item in items:
        (year, month, day) = item[0].split("-")
        itemdate = date(int(year), int(month), int(day))
        # week_1 teschtet öb ds scho isch vergäh worde, wenn nid de machter das häre
        if itemdate <= date.today() + timedelta(7) and not week_1:
            output.add_field(name="__BIS NÄCHSTE WOCHE:__",
                             value=f"(Bis zum {date.today() + timedelta(7)})",
                             inline=False)
            week_1 = True

        if date.today() + timedelta(7) <= itemdate <= date.today() + timedelta(14) and not week_2:
            output.add_field(name="__NÄCHSTE 2 WOCHEN:__",
                             value=f"(Bis zum {date.today() + timedelta(14)})")
            week_2 = True

        if date.today() + timedelta(14) <= itemdate <= date.today() + timedelta(30) and not month_1:
            output.add_field(name="__INNERHALB VON 30 TAGEN:__",
                             value=f"(Bis zum {date.today() + timedelta(30)})")
            month_1 = True

        if date.today() + timedelta(30) <= itemdate <= date.today() + timedelta(60) and not month_2:
            output.add_field(name="__INNERHALB VON 60 TAGEN:__",
                             value=f"(Bis zum {date.today() + timedelta(60)})")
            month_2 = True

        if date.today() + timedelta(60) <= itemdate and not future:
            lastitem = items[-1][0].split("-")
            output.add_field(name="__SPÄTER ALS 60 TAGE:__",
                             value=f"(Bis zum {date(int(lastitem[0]), int(lastitem[1]), int(lastitem[2]))})")
            future = True

        desc = item[3]
        if len(desc) > 20:
            desc = item[3][:20]+"..."  # wöu schüsch chasch du lernziele ha wo viu ds läng si.

        output.add_field(name=f" {item[1].capitalize()} {item[2]}",
                         value=f" {str(weekdays[itemdate.weekday()])}, "
                               f"{day}.{month}.{year}\n {desc}\n ",
                         inline=False)

        output.set_footer(text=footer)
    return output
