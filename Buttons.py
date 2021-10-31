import nextcord

class PageButtons(nextcord.ui.View):  # buttons für d siitene
    def __init__(self, results, currentpage):
        super().__init__(timeout=120.0)  # timeout macht eifach das d buttons nach 2 minute nümme chöi drückt wärde.
        self.currentpage = currentpage
        self.results = results
        self.left = False
        self.right = False
        self.select = 0

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


class Selectionmode(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=120.0)
        self.edit = False
        self.delete = False

    @nextcord.ui.button(label="Edit", style=nextcord.ButtonStyle.primary, disabled=True)
    async def edit(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.edit = True
        self.stop()

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red)
    async def delete(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.delete = True
        self.stop()


class Confirmdelete(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=120.0)
        self.delete = False

    @nextcord.ui.button(label="Yes", style=nextcord.ButtonStyle.red)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.delete = True
        self.stop()

    @nextcord.ui.button(label="No", style=nextcord.ButtonStyle.green)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.delete = False
        self.stop()