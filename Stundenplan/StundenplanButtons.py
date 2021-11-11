"""Ds wird uf iis gleit"""

import nextcord


async def testinter(interaction, ctx):
    if interaction.user != ctx.author:
        await interaction.response.send_message("Du kannst dieses Dialogfeld nicht benutzen", ephemeral=True)
        return False
    return True

mylist = (("MO", 1), ("MO", 2), ("MO", 3), ("MO", 5))
control = (1, 2, 3, 4, 5)
days = ("MO", "DI", "MI", "DO", "FR")


class TestButton(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.pressedbtn = ""
        self.ispressed = False
        mylistcopy = mylist
        for i in self.children:
            i.disabed = False
            i.style = nextcord.ButtonStyle.grey
            buttonid = i.__getattribute__("custom_id").split(":")
            for j in mylistcopy:
                print(list(j), buttonid)
                if j[0] == buttonid[0] and str(j[1]) == buttonid[1]:
                    i.style = nextcord.ButtonStyle.primary

    @nextcord.ui.button(label="A", style=nextcord.ButtonStyle.red, custom_id="MO:1",  disabled=False, row=1)
    async def Mo1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if await testinter(interaction, self.ctx):
            self.pressedbtn = button.custom_id
            self.ispressed = True