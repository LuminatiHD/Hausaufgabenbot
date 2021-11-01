import nextcord


async def testinter(interaction, ctx):
    if interaction.user != ctx.author:
        await interaction.response.send_message("Du kannst dieses Dialogfeld nicht benutzen", ephemeral=True)
        return False
    return True


class PageButtons(nextcord.ui.View):  # buttons für d siitene
    """"Diese Buttons sind für den outlook-command. Dabei hat es 5 select-buttons (mit welchen man ein bestimmtes
    Element vom Outlook auswählen kann), sowie 4 Buttons fürs blättern. Dabei gibt es jeweils einen knopf für 1 Seite
    weiter zurück, sowie je einen Knopf für ganz nach hinten/vorne."""

    def __init__(self, results, currentpage, ctx):
        super().__init__(timeout=None)  # timeout macht eifach das d buttons nach 2 minute nümme chöi drückt wärde.
        self.currentpage = currentpage
        self.ctx = ctx
        self.results = results
        self.left = False
        self.right = False
        self.select = 0
        self.bigleft.disabled = self.currentpage == 0
        self.leftbutton.disabled = self.currentpage == 0
        self.rightbutton.disabled = (self.currentpage + 1) >= len(results) / 5 # mit [BUTTON].disabled chame d disability vomne button wächsle. det machi hie für dasme nit cha out of bounds gah.
        self.bigright.disabled = (self.currentpage + 1) >= len(results) / 5
        for button in self.children:
            label = button.__str__().split(" ")[5].split("=")[1][1:-1]
            if label not in ["<<", "<", ">", ">>"] and int(label) > len(results)-(currentpage*5): # wider zum prevente das me out of bounds geit, i däm fau das me nid iwie ds item 4 selected wo gar nid da isch.
                 button.disabled = True

    @nextcord.ui.button(label="1", style=nextcord.ButtonStyle.primary)
    async def Select1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.select = 0
            self.stop()

    @nextcord.ui.button(label="2", style=nextcord.ButtonStyle.primary)
    async def Select2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.select = 1
            self.stop()

    @nextcord.ui.button(label="3", style=nextcord.ButtonStyle.primary)
    async def Select3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.select = 2
            self.stop()

    @nextcord.ui.button(label="4", style=nextcord.ButtonStyle.primary)
    async def Select4(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.select = 3
            self.stop()

    @nextcord.ui.button(label="5", style=nextcord.ButtonStyle.primary)
    async def Select5(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.select = 4
            self.stop()

    @nextcord.ui.button(label="<<", style=nextcord.ButtonStyle.primary)
    async def bigleft(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.currentpage = 0
            self.left = True
            self.stop()

    @nextcord.ui.button(label="<", style=nextcord.ButtonStyle.primary)
    async def leftbutton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.currentpage -= 1
            self.left = True
            self.stop()

    @nextcord.ui.button(label=">", style=nextcord.ButtonStyle.primary)
    async def rightbutton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.currentpage += 1
            self.right = True
            self.stop()

    @nextcord.ui.button(label=">>", style=nextcord.ButtonStyle.primary)
    async def bigright(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.currentpage = int(len(self.results)/5) + (len(self.results) % 5>0)-1
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
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.confirm = True
            self.stop()

    @nextcord.ui.button(label="Nein", style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
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

    @nextcord.ui.button(label="A", style=nextcord.ButtonStyle.primary)
    async def Hausaufgabe(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.choice = "Hausaufgabe"
            self.stop()

    @nextcord.ui.button(label="B", style=nextcord.ButtonStyle.primary)
    async def Test(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.choice = "Test"
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

    @nextcord.ui.button(label="Für Alle", style=nextcord.ButtonStyle.primary)
    async def All(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.access = "all"
            self.stop()

    @nextcord.ui.button(label="Für mein SF", style=nextcord.ButtonStyle.primary)
    async def OnlySF(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            SF = "all"
            for role in self.ctx.author.roles:
                if role.name.lower().startswith("sf"):
                    SF = role.name

            self.access = SF
            self.stop()

    @nextcord.ui.button(label="Für mein EF", style=nextcord.ButtonStyle.primary)
    async def OnlyEF(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            EF = "all"
            for role in self.ctx.author.roles:
                if role.name.lower().startswith("ef"):
                    EF = role.name

            self.access = EF
            self.stop()

            self.access = EF
            self.stop()

    @nextcord.ui.button(label="Nur für mich", style=nextcord.ButtonStyle.primary)
    async def Private(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(ctx=self.ctx, interaction=interaction):
            self.access = "private"
            self.stop()

