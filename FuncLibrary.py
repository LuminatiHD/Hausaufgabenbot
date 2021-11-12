import nextcord
from datetime import timedelta, date

weekdays = ["Montag",
            "Dienstag",
            "Mittwoch",
            "Donnerstag",
            "Freitag",
            "Samstag",  # es git vor datetime-library ä command wo tuet dr wuchetag vomne datum zrüggäh,
            "Sonntag"]  # allerdings nur aus integer. Ds isch für ds formatting.

StP_colors = {"Deutsch":0xffdd00,
              "Geschichte":0xcc8904,
              "Englisch":0xff0011,
              "Math":0x097dd6,
              "Franz":0x09a6d6,
              "Physik":0x2847ad,
              "Bio":0x0eab25,
              "Chemie":0x1adbce,
              "Sport":0xdb241a,
              "MINT":0xe1e2eb,
              "Musik":0x1bd18e,
              "BG":0x9f11c2,
              "SF Physik": 0x041859,
              "SF AM": 0x5e0303,
              "SF Bio":0x06701d,
              "SF Chemie":0x08d134,
              "SF Wirtschaft": 0xe01094,
              "SF Recht": 0xe010cf,
              "EF Musik":0xdbce14,
              "EF Geschichte":0xa85507,
              "EF Info":0x10e0c5,
              "EF PP":0xe0103a,
              "SF Philo":0xb80b6a,
              "SF PP":0xf72fc9,
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
                             value=f"(Bis zum {date.today() + timedelta(14)})", inline=False)
            week_2 = True

        if date.today() + timedelta(14) < itemdate <= date.today() + timedelta(30) and not month_1:
            output.add_field(name="__INNERHALB VON 30 TAGEN:__",
                             value=f"(Bis zum {date.today() + timedelta(30)})", inline=False)
            month_1 = True

        if date.today() + timedelta(30) < itemdate <= date.today() + timedelta(60) and not month_2:
            output.add_field(name="__INNERHALB VON 60 TAGEN:__",
                             value=f"(Bis zum {date.today() + timedelta(60)})", inline=False)
            month_2 = True

        if date.today() + timedelta(60) < itemdate and not future:
            lastitem = items[-1][0].split("-")
            output.add_field(name="__SPÄTER ALS 60 TAGE:__",
                             value=f"(Bis zum {date(int(lastitem[0]), int(lastitem[1]), int(lastitem[2]))})", inline=False)
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
