import nextcord
from nextcord.ext.commands.context import Context
from datetime import date, datetime, timedelta
import json

maxdayspermonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


async def testinter(interaction, ctx):
    if interaction.user != ctx.author:
        await interaction.response.send_message("Du kannst dieses Dialogfeld nicht benutzen", ephemeral=True)
        return False
    return True


class TestButtons(nextcord.ui.View):
    """Dieses Objekt dient nur als Beispiel und wird nirgends verwendet."""

    def __init__(self, ctx):
        """Weis nonid so ganz was das macht, aber es bruuchts zum ä button z kreiere. Wenis richtig verstande ha de
        heisst z super() eifach, dass me ds __init__ vor Superlass (ä class a mitere superclass b heisst, a isch ä
        subclass vo b. Üsi superclass isch d class nextcord.ui.View)"""
        super().__init__(timeout=120.0)
        self.ctx = ctx
        if self.ctx.message.content.startswith("bababooey"):
            self.MyButton.disabled = True
        """ Hie heimer jetz ä attribute vomne button gänderet. Wie genau das geit gsehmer unge."""

    """Ds dört unge isch ä decorator. Dä nimmt die funkion womer unge definiert hei, und macht när sozäge dass des imne button 
    integriert isch. Wie genau ds funktioniert isch nid so wichtig, wichtig si d argumänt wome cha drigäh: 
     - ds label definiert, was när ufem button wird stah.
     - weme statt text es emoji möcht, chame ds mitem argumänt 'emoji' mache.
     - mitem 'style' chame d farbe bestimme. D farbe si immer nextcord.ButtonStyle.[COLOR]. es git 6 farbe:
         - red/danger: Rot
         - green/success: grüen
         - blurple/primary: blau
         - grey/gray/secondary: grau
         - url/link: Isch spezieu wöuses nid ä farb isch, sondern ä link, heisst, weme dä chnopf drückt, 
                     dass die URL göffnet wird (ka wie genau me ds när implementiert tbh).
     - mit custom_id 
     - disabled: disabled nimmt ä boolean value. We ä button disabled isch, de chame nä nümme drücke.
       mä cha aber ä button nid ire button-funkion disable. Mä cha aber buttons usserhaub disable, wiemer obe hei gseh.
       mä cha ou ä button usserhaub vor class disable, aso wemer es buttonobject Button=TestButtons(ctx) hei, de 
       chöimer mit
          Button.nameofbutton.disabled = True
        dr button nameofbutton disable.
     - mit row chame die jewilige buttons vomne buttonobject ordne. hani nie bruucht.
     Fyi, mä cha i decorator nid argumänt inegäh wo ir buttonclass definiert si."""

    @nextcord.ui.button(label="A", emoji="😶", style=nextcord.ButtonStyle.red, custom_id="ID", disabled=False, row=1)
    async def MyButton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """interaction funkioniert praktisch so wie ctx. mä cha drvo usefinge wär ses drückt het, wo etc. """
        if await testinter(ctx=self.ctx, interaction=interaction):
            """d funkion testinter teschtet eifach öb dr button vom gliiche mönsch isch drückt worde wo het dr button 
            verlangt."""
            self.stop()
            """self.stop() heisst, d class höret uf z runne, aso nimmt keni inputs meh. Ds isch hiufriich weme 
            usserhaub vor class sitzet. Wöu weme es Buttonobject Button kreiert, de chame mit
              await Button.wait()
            druf warte, dass dr button stoppet. Mä chönnti zwar vilech es attribute self.ispressed oder so mache, 
            de muesme dr button ou nid neu generiere weme dr button mehrmaus bruucht."""


class PageButtons(nextcord.ui.View):  # buttons für d siitene
    """"Diese Buttons sind für den outlook-command. Dabei hat es 5 select-buttons (mit welchen man ein bestimmtes
    Element vom Outlook auswählen kann), sowie 4 Buttons fürs blättern. Dabei gibt es jeweils einen knopf für 1 Seite
    weiter zurück, sowie je einen Knopf für ganz nach hinten/vorne."""

    def __init__(self, results, currentpage, ctx):
        super().__init__(timeout=120)  # timeout macht eifach das d buttons nach 2 minute nümme chöi drückt wärde.
        self.currentpage = currentpage
        self.ctx = ctx
        self.results = results
        self.left = False
        self.right = False
        self.select = -1
        self.bigleft.disabled = self.currentpage == 0
        self.leftbutton.disabled = self.currentpage == 0
        self.rightbutton.disabled = (self.currentpage + 1) >= len(results) / 5
        self.bigright.disabled = (self.currentpage + 1) >= len(results) / 5
        # mit [BUTTON].disabled chame d disability vomne button wächsle.
        # das machi hie für dasme nit cha out of bounds gah.

        for i in range(1, 5+1):
            self.add_item(TimeButton(self, self.ctx, str(i), "select", row=0))

        for button in self.children:
            label = button.__str__().split(" ")[5].split("=")[1][1:-1]
            if label not in ["<<", "<","o", ">", ">>"] and int(label) > len(results) - (currentpage * 5):
                button.disabled = True

    @nextcord.ui.button(label="<<", style=nextcord.ButtonStyle.primary, row=1)
    async def bigleft(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.currentpage = 0
            self.left = True
            self.stop()

    @nextcord.ui.button(label="<", style=nextcord.ButtonStyle.primary, row=1)
    async def leftbutton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.currentpage -= 1
            self.left = True
            self.stop()

    @nextcord.ui.button(label="o", style=nextcord.ButtonStyle.primary, row=1)
    async def endinteraction(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.stop()

    @nextcord.ui.button(label=">", style=nextcord.ButtonStyle.primary, row=1)
    async def rightbutton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.currentpage += 1
            self.right = True
            self.stop()

    @nextcord.ui.button(label=">>", style=nextcord.ButtonStyle.primary, row=1)
    async def bigright(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.currentpage = int(len(self.results) / 5) + (len(self.results) % 5 > 0) - 1
            self.right = True
            self.stop()


class Selectionmode(nextcord.ui.View):
    """
    Wenn man ein Item mit den obrigen knöpfen ausgewählt hat, kann man hier auswählen, was man mite dem Item tun will.
    Es gibt einen Knopf, um das Element zu löschen, einen um es zu editieren und einen zum wieder zur outlook-sicht
    zurückzugelangen."""

    def __init__(self, ctx):
        super().__init__(timeout=120.0)
        self.edit = False
        self.delete = False
        self.goback = False
        self.ctx = ctx

    @nextcord.ui.button(label="Edit", style=nextcord.ButtonStyle.primary)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.edit = True
            self.stop()

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.delete = True
            self.stop()

    @nextcord.ui.button(label="Go back", style=nextcord.ButtonStyle.grey)
    async def goback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.goback = True
            self.stop()


class Confirm(nextcord.ui.View):
    """
    Fragt nach einer Bestätigung für etw.
    """

    def __init__(self, ctx):
        super().__init__(timeout=120.0)
        self.confirm = False
        self.ctx = ctx

    @nextcord.ui.button(label="Ja", style=nextcord.ButtonStyle.green)
    async def confirmbtn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.confirm = True
            self.stop()

    @nextcord.ui.button(label="Nein", style=nextcord.ButtonStyle.red)
    async def cancelbtn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.confirm = False
            self.stop()


class EditButtons(nextcord.ui.View):
    """Das ist für das Editieren eines Items. Mit den unteren Knöpfen fragt man nach, was man genau editieren möchte."""

    def __init__(self, ctx):
        super().__init__(timeout=120.0)
        self.edit = []
        self.goback = False
        self.ctx = ctx

    @nextcord.ui.button(label="Kategorie", style=nextcord.ButtonStyle.primary)
    async def kategorie(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.edit.append("kategorie")
            self.stop()

    @nextcord.ui.button(label="Aufgabe", style=nextcord.ButtonStyle.primary)
    async def aufgabe(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.edit.append("aufgabe")
            self.stop()

    @nextcord.ui.button(label="Datum", style=nextcord.ButtonStyle.primary)
    async def datum(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.edit.append("datum")
            self.stop()

    @nextcord.ui.button(label="Fach", style=nextcord.ButtonStyle.primary)
    async def fach(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.edit.append("fach")
            self.stop()

    @nextcord.ui.button(label="Zugriff", style=nextcord.ButtonStyle.primary)
    async def access(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.edit.append("access")
            self.stop()

    @nextcord.ui.button(label="Zurück", style=nextcord.ButtonStyle.gray)
    async def goback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.goback = True
            self.stop()


class TestOrHA(nextcord.ui.View):
    """Diese Knöpfe sind da für wenn man ein neues Item erstellen will. Diese beiden Buttons fragen nach, ob man einen
    Test oder eine Hausaufgabe eintragen will."""

    def __init__(self, ctx):
        super().__init__(timeout=120.0)
        self.choice = "Hausaufgabe"
        self.ctx = ctx
        self.exit = False

    @nextcord.ui.button(label="Hausaufgabe", style=nextcord.ButtonStyle.primary)
    async def Hausaufgabe(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.choice = "Hausaufgabe"
            self.stop()

    @nextcord.ui.button(label="Test", style=nextcord.ButtonStyle.primary)
    async def Test(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.choice = "Test"
            self.stop()

    @nextcord.ui.button(label="Unspezifisch", style=nextcord.ButtonStyle.primary)
    async def Nocateg(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.choice = ""
            self.stop()

    @nextcord.ui.button(label="Abbrechen", style=nextcord.ButtonStyle.red)
    async def Exit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.exit=True
            self.stop()


class ManageItemAccess(nextcord.ui.View):
    """Wird geregelt wer dieses Item sehen kann, aka ob es privat ist,
    für alle, oder nur für die jeweiligen SF oder EF."""

    def __init__(self, ctx):
        super().__init__(timeout=120.0)
        self.ctx = ctx
        self.access = "all"

        # wede diräkt mitem bot redisch, de chaner d ufgab nid uf SF oder EF restricte wöuer d serverdate nid het.
        if self.ctx.channel.__str__().startswith("Direct Message"):
            self.OnlyEF.disabled = True
            self.OnlySF.disabled = True
            self.OnlyKF.disabled = True

    @nextcord.ui.button(label="Für Alle", style=nextcord.ButtonStyle.primary)
    async def All(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.access = "all"
            self.stop()

    @nextcord.ui.button(label="Für mein SF", style=nextcord.ButtonStyle.primary)
    async def OnlySF(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            sf = "all"
            for role in self.ctx.author.roles:
                if role.name.lower().startswith("sf"):
                    sf = role.name

            self.access = sf
            self.stop()

    @nextcord.ui.button(label="Für mein EF", style=nextcord.ButtonStyle.primary)
    async def OnlyEF(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            ef = "all"
            for role in self.ctx.author.roles:
                if role.name.lower().startswith("ef"):
                    ef = role.name

            self.access = ef
            self.stop()

    @nextcord.ui.button(label="Für mein KF", style=nextcord.ButtonStyle.primary)
    async def OnlyKF(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            kf = "all"
            for role in self.ctx.author.roles:
                if role.name.lower().startswith("kf"):
                    kf = role.name
            self.access = kf
            self.stop()

    @nextcord.ui.button(label="Nur für mich", style=nextcord.ButtonStyle.primary)
    async def Private(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.access = "private"
            self.stop()


class ChooseWeekdays(nextcord.ui.View):
    def __init__(self, ctx: Context, confirmbtn:bool = False):
        super().__init__(timeout=120.0)
        self.ctx = ctx
        self.choice = None
        self.confirm = False

        self.confirmbtn.disabled = confirmbtn

        for i in ("mo", "di", "mi", "do", "fr", "sa", "so"):
            self.add_item(TimeButton(self, self.ctx, i.capitalize(), "choice"))

    @nextcord.ui.button(label="Bestätigen", style=nextcord.ButtonStyle.red, row=3)
    async def confirmbtn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.confirm = True
            self.stop()


class ChooseTime(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120.0)
        self.ctx = ctx
        self.confirm= False
        self.choice=None

        for i in range(6, 21):
            self.add_item(TimeButton(self, ctx, f"{i}:00", "choice", row=(i-6)//5))

    @nextcord.ui.button(label="Bestätigen", style=nextcord.ButtonStyle.red, row=4)
    async def confirmbtn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.confirm = True
            self.stop()


class TimeButton(nextcord.ui.Button):
    def __init__(self, view_obj, ctx, label, attr, row=None):
        super().__init__(style=nextcord.ButtonStyle.primary, label=label, row=row)
        self.ctx = ctx
        self.view_obj = view_obj
        self.attr = attr

    async def callback(self, interaction: nextcord.Interaction):
        if await testinter(interaction=interaction, ctx=self.ctx):
            self.view_obj.__setattr__(self.attr, self.label)
            self.view_obj.stop()


class choose_SF(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120.0)
        self.ctx = ctx
        self.sf = 'all'

    @nextcord.ui.button(label="PAM", style=nextcord.ButtonStyle.primary)
    async def pam(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.sf = 'SF PAM'
            self.stop()

    @nextcord.ui.button(label="BC", style=nextcord.ButtonStyle.primary)
    async def bc(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.sf = 'SF BC'
            self.stop()

    @nextcord.ui.button(label="PPP", style=nextcord.ButtonStyle.primary)
    async def ppp(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.sf = 'SF PPP'
            self.stop()

    @nextcord.ui.button(label="WR", style=nextcord.ButtonStyle.primary)
    async def wr(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.sf = 'SF WR'
            self.stop()


class choose_EF(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120.0)
        self.ctx = ctx
        self.ef = 'all'

    @nextcord.ui.button(label="Info", style=nextcord.ButtonStyle.primary)
    async def info(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.ef = 'EF Info'
            self.stop()

    @nextcord.ui.button(label="Geschichte", style=nextcord.ButtonStyle.primary)
    async def history(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.ef = 'EF Geschichte'
            self.stop()

    @nextcord.ui.button(label="PP", style=nextcord.ButtonStyle.primary)
    async def pp(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.ef = 'EF PP'
            self.stop()

    @nextcord.ui.button(label="Smeder (Chemie)", style=nextcord.ButtonStyle.primary)
    async def smedi(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.ef = 'EF Chemie'
            self.stop()

    @nextcord.ui.button(label="Musik", style=nextcord.ButtonStyle.primary)
    async def musik(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.ef = 'EF Musik'
            self.stop()

    @nextcord.ui.button(label="Sport", style=nextcord.ButtonStyle.primary)
    async def sport(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.ef = 'EF Sport'
            self.stop()


class choose_KF(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120.0)
        self.ctx = ctx
        self.kf = 'all'

    @nextcord.ui.button(label="Musik", style=nextcord.ButtonStyle.primary)
    async def musik(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.kf = 'KF Musik'
            self.stop()

    @nextcord.ui.button(label="BG", style=nextcord.ButtonStyle.primary)
    async def bg(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.kf = 'KF BG'
            self.stop()


class BriefingSettings(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout = 180)
        self.ctx = ctx
        self.choice = None

    @nextcord.ui.button(label="Zeiten ändern", style=nextcord.ButtonStyle.primary)
    async def edit_time(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        if await testinter(interaction, self.ctx):
            self.choice = "time"
            self.stop()

    @nextcord.ui.button(label="o", style=nextcord.ButtonStyle.primary)
    async def delmsg(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        if await testinter(interaction, self.ctx):
            self.choice = None
            self.stop()

    @nextcord.ui.button(label="Fächer ändern", style=nextcord.ButtonStyle.primary)
    async def edit_classes(self, button:nextcord.ui.Button, interaction:nextcord.Interaction):
        if await testinter(interaction, self.ctx):
            self.choice = "classes"
            self.stop()


class Dropdown(nextcord.ui.Select):
    def __init__(self):
        options = [nextcord.SelectOption(label=str(i)) for i in range(1, 25)]
        super().__init__(placeholder="ur mom:", max_values=1, min_values=1, options=options)


class DayDropdown(nextcord.ui.Select):
    def __init__(self, menu, day):
        self.menu = menu

        if day is None or day == "<25" or day<"25":
            options = [nextcord.SelectOption(label=str(i)) for i in range(1, 25)] \
                      + [nextcord.SelectOption(label=">24", description="Discord erlaubt nur 25 Optionen max")]
        else:
            options = [nextcord.SelectOption(label="<25")]+\
                      [nextcord.SelectOption(label=str(i)) for i in range(25, 32)] \


        super().__init__(placeholder="Tag:", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if await testinter(interaction, self.menu.ctx):
            self.menu.day = self.values[0]
            if self.values[0] == ">24" or self.values[0] == "<25":
                self.menu.stop()


class ChooseDatum(nextcord.ui.View):
    def __init__(self, ctx, day=None, month=None, year=None,
                 year_bounds:tuple[int, int] = (datetime.now().year, datetime.now().year+3)):
        self.exit = False
        self.ctx = ctx
        self.update = True
        self.over = False
        super().__init__(timeout = 120)

        self.day = day
        self.month = month
        self.year = year

        today = (datetime.utcnow()+timedelta(hours=2))

        dayselect = DayDropdown(self, self.day)
        dayselect.custom_id = "day"

        monthselect = Dropdown()
        monthselect.placeholder = "Monat:"
        monthselect.options = [nextcord.SelectOption(label=str(i)) for i in range(1, 13)]
        monthselect.custom_id = "month"

        yearselect = Dropdown()
        yearselect.placeholder = "Jahr:"
        yearselect.options = [nextcord.SelectOption(label=str(i)) for i in range(*year_bounds)]
        yearselect.custom_id = "year"

        self.add_item(dayselect)
        self.add_item(monthselect)
        self.add_item(yearselect)

    @nextcord.ui.button(label="Bestätigen", style=nextcord.ButtonStyle.primary, custom_id = "confirm")
    async def confirm(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if await testinter(interaction, self.ctx) and all(i.values for i in self.children if
                                                          type(i) == Dropdown or type(i) == DayDropdown):

            for i in self.children:
                if i.custom_id == "day":
                    self.day = int(i.values[0])

                elif i.custom_id == "month":
                    self.month = int(i.values[0])

                elif i.custom_id == "year":
                    self.year = int(i.values[0])

            if int(self.day) > maxdayspermonth[int(self.month)-1]:
                self.day = maxdayspermonth[int(self.month)-1]
                if int(self.month) == 2 and not (self.year%4==0
                                                 and not (self.year%100==0
                                                          and not (self.year%400==0))):
                    self.day = 28

            self.exit = False
            self.over = True
            self.stop()

    @nextcord.ui.button(label="Abbrechen", style=nextcord.ButtonStyle.red, custom_id="exit")
    async def goback(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if await testinter(interaction, self.ctx):
            self.over = True
            self.exit = True
            self.stop()


class Poll_Button(nextcord.ui.Button):
    def __init__(self, label, view_obj, duration):
        super().__init__()
        self.label = label
        self.over = datetime.now()+timedelta(seconds=duration)
        self.style = nextcord.ButtonStyle.blurple
        self.view_obj = view_obj

    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user.id in self.view_obj.voters.keys() \
                and self.view_obj.voters[interaction.user.id] != self.label:
            await interaction.response.send_message("Dein Vote wurde geändert", ephemeral=True)

        self.view_obj.voters[interaction.user.id] = self.label

        if datetime.now()> self.over:
            self.view_obj.stop()


class Poll_ViewObj(nextcord.ui.View):
    def __init__(self, options, duration):
        super().__init__(timeout=duration)
        self.voters = {}
        for opt in options:
            self.add_item(Poll_Button(label=opt, view_obj=self, duration=duration))


class Vote_btns(nextcord.ui.View):
    def __init__(self, flair, voters=dict()):
        super().__init__(timeout=60)
        self.flair = flair
        self.voters = voters

        if not self.flair:
            self.flair = "null"

        # btn = nextcord.ui.Button()
        # btn.label = "Zurück"
        # btn.row = 2
        # self.add_item(btn)

    async def change_score(self, val, voter, inter):
        if not voter in self.voters.keys() or self.voters[voter]!=val:
            with open("News/tag_priority.json", "r") as file:
                in_file = json.load(file)
                try:
                    if voter in self.voters.keys():
                        in_file[self.flair] += 2*val
                    else:
                        in_file[self.flair] += val

                except KeyError:
                    in_file[self.flair] = val

                with open("News/tag_priority.json", "w") as out_file:
                    json.dump(in_file, out_file)

            self.voters[voter] = val

        else:
            await inter.response.send_message(f"Du hast schon {self.voters[voter]} gewählt", ephemeral=True)

    @nextcord.ui.button(emoji="👍", style=nextcord.ButtonStyle.green, row=1)
    async def up(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.change_score(1, interaction.user.id, interaction)

    @nextcord.ui.button(emoji="👎", style=nextcord.ButtonStyle.red, row=1)
    async def down(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.change_score(-1, interaction.user.id, interaction)

    @nextcord.ui.button(label="Zurück", row=2)
    async def back(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.stop()


class Select_article(nextcord.ui.View):
    def __init__(self, posts):
        super().__init__(timeout=120)
        self.choice = None
        self.add_item(menu(posts, self))


class menu(nextcord.ui.Select):
    def __init__(self, posts, view_obj):
        options = [nextcord.SelectOption(label=i) for i in posts.keys()]
        super().__init__(placeholder="Artikel", min_values=1, max_values=1,  options=options)
        self.view_obj = view_obj

    async def callback(self, interaction: nextcord.Interaction):
        self.view_obj.choice = self.values[0]
        self.view_obj.stop()


class CollapseBtn(nextcord.ui.Button):
    def __init__(self):
        super().__init__(style=nextcord.ButtonStyle.primary, label="Einklappen", row=2)
        self.collapse = False

    async def callback(self, interaction: nextcord.Interaction):
        self.collapse = True
        self.view.stop()


class Dropdown_Menu(nextcord.ui.View):
    def __init__(self, ctx, options, min=1, max=1):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.dropdown = nextcord.ui.Select(min_values=min, max_values=max,
                                           options = [nextcord.SelectOption(label=i) for i in options])
        self.add_item(self.dropdown)
        self.output = []
        self.goback = False

    @nextcord.ui.button(label="Bestätigen", style=nextcord.ButtonStyle.primary)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(interaction, self.ctx):
            self.output = self.dropdown.values
            self.stop()

    @nextcord.ui.button(label="Abbrechen", style=nextcord.ButtonStyle.red)
    async def goback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(interaction, self.ctx):
            self.goback = True
            self.stop()