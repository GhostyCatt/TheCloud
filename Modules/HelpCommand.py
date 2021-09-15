# Library Imports
import nextcord, json
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *
from Tools.HelpView import *
from Tools.Dismiss import Dismiss

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Variables
cog_ignore = ["Isolated Commands", "CommandErrorHandler", "Greetings"]

# Help command subclass
class Help(commands.HelpCommand):
    """
    The Help Command
    ---------------
    Types: 
    * Bot Help
    * Command Help
    * Cog Help
    * Group Help
    """
    def get_command_signature(self, command):
        """Get a clean command usage string"""
        prefix = Options['Prefix']
        return '%s%s %s' % (prefix, command.qualified_name, command.signature)


    async def send_bot_help(self, mapping):
        """Send overall help"""
        channel = self.get_destination()
        prefix = Options['Prefix']

        # Create Embed
        embed = await Custom(
            f"The Cloud", 
            f"For more help on specific modules, use the command `{prefix}help <module>` or `{prefix}help <command>`, or pick the module from the menu below."
        )

        # Add a new field for every cog in the bot
        for cog, commands in mapping.items():
            name = getattr(cog, "qualified_name", "Isolated Commands")

            if name in cog_ignore:
                pass
            else:
                embed.add_field(name = f"**{name}** [{len(commands)}]", value = f"`{prefix}help {name}`", inline = True)
        
        # Set embed footer
        embed.set_footer(text = "The buttons on this command will stop working after 30 seconds.")
        
        # Send embed with button interactions
        view = ButtonArrayMain(self.context, mapping, self, embed)
        view.response = await channel.send(embed = embed, view = view)


    async def send_cog_help(self, cog):
        """Send module specific help"""
        channel = self.get_destination()
        prefix = Options['Prefix']

        # Get module name / description
        name = getattr(cog, "qualified_name", "No Category")
        description = getattr(cog, "description", "No description provided")

        # Create Embed
        embed = await Custom(f"{name}", f"{description}\n\nUse the command `{prefix}help <command>` or `{prefix}help <module>` for more.")
        
        # Add a new field for each command in the module
        for command in cog.walk_commands():
            if command.parent != None:
                pass
            else:
                name = getattr(command, "name", "CommandName")
                description = getattr(command, "help", "No description provided")

                embed.add_field(name = f"**{name}**", value = f"> {command.help}", inline = False)
        
        # Send embed with button interactions
        view = ButtonArray(self.context)
        view.response = await channel.send(embed = embed, view = view)


    async def send_command_help(self, command):
        """Send command specific help"""
        channel = self.get_destination()
        prefix = Options['Prefix']

        # Get command info
        name = getattr(command, "name", "No name provided")
        description = getattr(command, "help", "No description provided")
        usage = getattr(command, "signature", "")
        aliases = getattr(command, "aliases", "None")

        # Create Embed
        embed = await Custom(f"{name.capitalize()}", f"**{description}**\n\n**Usage** » `{prefix}{name.lower()} {usage}`\n**Aliases** » `{aliases}`")
         
        # Send embed with button interactions
        view = ButtonArray(self.context)
        view.response = await channel.send(embed = embed, view = view)


    async def send_group_help(self, group):
        """Send grouped command help"""
        channel = self.get_destination()
        prefix = Options['Prefix']

        # Get command info
        name = getattr(group, "name", "No name provided")
        description = getattr(group, "help", "No description provided")

        # Create Embed
        embed = await Custom(f"{name.capitalize()}", f"**{description}**")

        # Add a field for every subcommand
        for command in group.commands:
            command = group.get_command(command.name)

            # Get subcommand info
            name = getattr(command, "name", "No name provided")
            description = getattr(command, "help", "No description provided")
            usage = getattr(command, "signature", "")
            aliases = getattr(command, "aliases", "None")

            embed.add_field(name = name, value = f"{description}\n**Usage** » `{prefix}{name.lower()} {usage}`\n**Aliases** » {aliases}", inline = False)
        
        # Send embed with button interactions
        view = ButtonArray(self.context)
        view.response = await channel.send(embed = embed, view = view)


    async def send_error_message(self, error):
        """Send error message in help command"""
        channel = self.get_destination()

        # Create Embed
        embed = await Custom(f"Error", f"{error}")

        # Send embed with button interactions
        view = Dismiss(self.context)
        view.response = await channel.send(embed = embed, view = view)