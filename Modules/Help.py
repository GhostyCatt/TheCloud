# Library Imports
import nextcord, json
from nextcord.embeds import Embed
from nextcord.ext import commands
from nextcord.ext.commands.core import Command

# Custom Imports
from Functions.Embed import *
from Views.Help import *
from Views.Dismiss import Dismiss

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Variables
cog_ignore = ["Isolated Commands", "CommandErrorHandler", "Greetings", "Tags", "Starboard"]

# Help command subclass
class Help(commands.HelpCommand):
    def get_command_signature(self, command):
        """Get a clean command usage string"""
        return '%s%s %s' % (Options['Prefix'], command.qualified_name, command.signature)

    async def get_select_options(self) -> list:
        """Get a list of options for the dropdown"""
        options = [
            nextcord.SelectOption(label = "Home", emoji = "🏠")
        ]

        for cog, command_set in self.get_bot_mapping().items():
            if not cog: pass
            else:
                filtered = await self.filter_commands(command_set, sort=True)
                if not filtered:
                    continue
                options.append(nextcord.SelectOption(
                    label = cog.qualified_name if cog else "No Category",
                    emoji = '🔍',
                )) 
        return options
    
    async def get_help_embed(self, mapping) -> nextcord.Embed:
        """Get bot help embed"""
        embed = await Custom(title = f"TheCloud Help", description = f"An enhanced minecraft experience.")
        for cog, command_set in mapping.items():
            if len(command_set) < 1: pass
            elif not cog: pass
            else: embed.add_field(name = getattr(cog, "qualified_name", "No Category"), value = f'`{Options["Prefix"]}help {getattr(cog, "qualified_name", "No Category")}`')

        embed.set_thumbnail(url = "https://cdn.discordapp.com/app-icons/886600985307410522/0a5e4d170d3603933f26e391c0573278.png?size=512")
        return embed

    async def get_cog_help_embed(self, cog:commands.Cog) -> nextcord.Embed:
        """Get cog help embed"""
        embed = await Custom(
            title = f"{cog.qualified_name if cog else 'No Category'} Commands",
            description = f"⚙️ {cog.description if cog.description else 'No description provided'}"
        )
        for command in cog.walk_commands():
            if isinstance(command, commands.Group): pass
            else: embed.add_field(name = command.name, value = command.help[:50] if command.help else "No description provided")
        
        embed.set_thumbnail(url = "https://cdn.discordapp.com/app-icons/886600985307410522/0a5e4d170d3603933f26e391c0573278.png?size=512")
        return embed
    

    async def get_command_help_embed(self, command:commands.Command) -> nextcord.Embed:
        """Get command help embed"""
        embed = await Custom(
            title = f"🛠️ {command.name.capitalize()}",
            description = command.help[:200] if command.help else 'No description provided'
        )
        embed.add_field(name = "Usage", value = f"`{self.get_command_signature(command)}`", inline = False)
        embed.add_field(name = "Aliases", value = "No aliases" if command.aliases == [] else command.aliases, inline = False)
        embed.add_field(name = "Enabled", value = "`✔️`" if command.enabled else '`❌`')
        embed.add_field(name = "Cooldown Active", value = "`✔️`" if command.is_on_cooldown(self.context) else '`❌`')
        embed.add_field(name = "Module", value = f"`{command.cog.qualified_name}`" if command.cog else '`No parent module`')
        embed.set_thumbnail(url = "https://cdn.discordapp.com/app-icons/886600985307410522/0a5e4d170d3603933f26e391c0573278.png?size=512")
        return embed
    
    async def get_group_help_embed(self, group:commands.Group) -> nextcord.Embed:
        """Get group help embed"""
        embed = await Custom(
            title = f"🛠️ {group.name.capitalize()}",
            description = group.help[:200] if group.help else 'No description provided'
        )
        embed.add_field(name = "Aliases", value = "No aliases" if group.aliases == [] else group.aliases, inline = False)
        embed.add_field(name = "Enabled", value = "✔️" if group.enabled else '`❌`')
        embed.add_field(name = "Cooldown Active", value = "✔️" if group.is_on_cooldown(self.context) else '`❌`')
        embed.add_field(name = "Module", value = f"`{group.cog.qualified_name}`" if group.cog else 'No parent module')

        subcommands = ''
        for subcommand in group.walk_commands():
            subcommands += f"{self.get_command_signature(subcommand)}\n"
        embed.set_thumbnail(url = "https://cdn.discordapp.com/app-icons/886600985307410522/0a5e4d170d3603933f26e391c0573278.png?size=512")
        return embed


    async def send_bot_help(self, mapping:str):
        """Send overall help"""
        embed = await self.get_help_embed(mapping)
        view = HelpView(self, await self.get_select_options())
        await self.context.channel.send(embed = embed, view = view)

    async def send_cog_help(self, cog:commands.Cog):
        """Send module specific help"""
        embed = await self.get_cog_help_embed(cog)
        await self.context.channel.send(embed = embed)

    async def send_command_help(self, command:commands.Command):
        """Send command specific help"""
        embed = await self.get_command_help_embed(command)
        await self.context.channel.send(embed = embed)

    async def send_group_help(self, group:commands.Group):
        """Send grouped command help"""
        embed = await self.get_group_help_embed(group)
        await self.context.channel.send(embed = embed)

    async def send_error_message(self, error):
        """Send error message in help command"""
        await Fail(error, self.context)