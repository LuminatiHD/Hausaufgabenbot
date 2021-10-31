import nextcord


class PageButtons(nextcord.ui.View):  # buttons für d siitene
    def __init__(self, results, currentpage):
        super().__init__(timeout=120.0)  # timeout macht eifach das d buttons nach 2 minute nümme chöi drückt wärde.
        self.currentpage = currentpage
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
        self.select = 0
        self.stop()

    @nextcord.ui.button(label="2", style=nextcord.ButtonStyle.primary)
    async def Select2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.select = 1
        self.stop()

    @nextcord.ui.button(label="3", style=nextcord.ButtonStyle.primary)
    async def Select3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.select = 2
        self.stop()

    @nextcord.ui.button(label="4", style=nextcord.ButtonStyle.primary)
    async def Select4(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.select = 3
        self.stop()

    @nextcord.ui.button(label="5", style=nextcord.ButtonStyle.primary)
    async def Select5(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.select = 4
        self.stop()

    @nextcord.ui.button(label="<<", style=nextcord.ButtonStyle.primary)
    async def bigleft(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.currentpage = 0
        self.left = True
        self.stop()

    @nextcord.ui.button(label="<", style=nextcord.ButtonStyle.primary)
    async def leftbutton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.currentpage -= 1
        self.left = True
        self.stop()

    @nextcord.ui.button(label=">", style=nextcord.ButtonStyle.primary)
    async def rightbutton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.currentpage += 1
        self.right = True
        self.stop()

    @nextcord.ui.button(label=">>", style=nextcord.ButtonStyle.primary)
    async def bigright(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.currentpage = int(len(self.results)/5) + (len(self.results) % 5>0)-1
        self.right = True
        self.stop()


class Selectionmode(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=120.0)
        self.edit = False
        self.delete = False
        self.goback = False

    @nextcord.ui.button(label="Edit", style=nextcord.ButtonStyle.primary)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.edit = True
        self.stop()

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.delete = True
        self.stop()

    @nextcord.ui.button(label="Go back", style=nextcord.ButtonStyle.grey)
    async def goback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.goback = True
        self.stop()


class Confirm(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=120.0)
        self.confirm = False

    @nextcord.ui.button(label="Yes", style=nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.confirm = True
        self.stop()

    @nextcord.ui.button(label="No", style=nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.confirm = False
        self.stop()


class EditButtons(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=120.0)
        self.edit = []
    @nextcord.ui.button(label="Kategorie", style=nextcord.ButtonStyle.primary)
    async def kategorie(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.edit.append("kategorie")
        self.stop()

    @nextcord.ui.button(label="Aufgabe", style=nextcord.ButtonStyle.primary)
    async def aufgabe(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.edit.append("aufgabe")
        self.stop()

    @nextcord.ui.button(label="Datum", style=nextcord.ButtonStyle.primary)
    async def datum(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.edit.append("datum")
        self.stop()

    @nextcord.ui.button(label="Fach", style=nextcord.ButtonStyle.primary)
    async def fach(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.edit.append("fach")
        self.stop()

class TestOrHA(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=120.0)
        self.choice = "Hausaufgabe"

    @nextcord.ui.button(label="A", style=nextcord.ButtonStyle.primary)
    async def Hausaufgabe(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = "Hausaufgabe"
        self.stop()

    @nextcord.ui.button(label="B", style=nextcord.ButtonStyle.primary)
    async def Test(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.choice = "Test"
        self.stop()