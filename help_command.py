import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context


class Help(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s %s' % (command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        """Zeigt diese Nachricht an"""
        embed = nextcord.Embed(title="Help")
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered if not self.get_command_signature(c).startswith("!")]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "Sonstige")
                embed.add_field(name=cog_name, value="\n".join(command_signatures))

            embed.set_footer(text="Zeige mit !help [COMMAND] Hilfe zu einem bestimmten Befehl an.")
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = nextcord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

