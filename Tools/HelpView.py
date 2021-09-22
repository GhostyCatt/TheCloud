# Library Imports
import nextcord, json
from nextcord.ui import button, View, Select

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Variables
cog_ignore = ["Isolated Commands", "CommandErrorHandler", "Greetings", "Tags", "Starboard"]

# Dropdown Menu for main help command
class Dropdown(Select):
    def __init__(self, ctx, mapping, helpcommand, homepage):
        self.ctx = ctx
        self.mapping = mapping
        self.help = helpcommand
        self.homepage = homepage

        # Options in select menu
        options = [
            nextcord.SelectOption(label = f'Home Page', description = f'Back to main home page.', value = 'Home')
        ]

        # Append cog options
        for cog, commands in mapping.items():
            name = getattr(cog, "qualified_name", "Isolated_Commands")
            description = getattr(cog, "description", "Stand-alone commands that exist outside of modules.")

            if name in cog_ignore:
                pass
            else:
                option = nextcord.SelectOption(label = f'{name} [{len(commands)}]', description = f'{description}', value = name)
                options.append(option)

        # Super init
        super().__init__(placeholder = 'Choose the module you want to check out', min_values = 1, max_values = 1, options = options)


    async def callback(self, interaction: nextcord.Interaction):
        """Module Specific Help"""
        for cog, commands in self.mapping.items():
            # Get command attributes
            cog_name = getattr(cog, "qualified_name", "Isolated_Commands")
            cog_description = getattr(cog, "description", "These commands exist outside of cogs.")
            
            if self.values[0] == cog_name:
                        
                command_signatures = [self.help.get_command_signature(c) for c in commands]
                if command_signatures:
                    commandslist = ""
                    for signature in command_signatures:
                        commandslist += f"\n`{signature}`"

                # Create embed and send
                embed = await Custom(f"{cog_name}", f"{cog_description}\n\n**Commands List**\n{commandslist}")
                await interaction.response.edit_message(embed = embed)
            
            elif self.values[0] == 'Home':
                # Send home page embed
                try:
                    await interaction.response.edit_message(embed = self.homepage)
                except: pass


# Button array for the main help command embed
class ButtonArrayMain(View):
    def __init__(self, ctx, mapping, helpcommand, homepage):
        super().__init__(timeout = 30)

        self.response = None
        self.ctx = ctx
        self.mapping = mapping
        self.help = helpcommand
        self.homepage = homepage
        
        self.add_item(nextcord.ui.Button(label = "Website", url = Options['Website']))
        self.add_item(Dropdown(self.ctx, self.mapping, self.help, self.homepage))
    

    @button(label = 'Minecraft IP\'s', style = nextcord.ButtonStyle.blurple)
    async def  dash_ips(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Send server ips from Assets"""
        with open('Assets/HelpIP.txt', 'r') as IPAsset:
            Ips = IPAsset.read()
        
        embed = await Custom("Server IP's", Ips)
        await interaction.response.send_message(embed = embed, ephemeral = True)


    @button(label = 'About Me', style = nextcord.ButtonStyle.blurple)
    async def  help_info(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Send bot Info from Assets"""
        with open('Assets/HelpInfo.txt', 'r') as InfoAsset:
            Info = InfoAsset.read()
        
        embed = await Custom("Info", Info)
        await interaction.response.send_message(embed = embed, ephemeral = True)


    @button(label = '❌', style = nextcord.ButtonStyle.red)
    async def  dash_cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Disable all interactions"""
        for child in self.children:
            child.disabled = True  
        await self.response.edit(view = self)
        
        self.stop()


    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass
    

    async def interaction_check(self, interaction: nextcord.Interaction):
        """Make it so that only the author can use the interactions"""
        return interaction.user.id == self.ctx.author.id


# Button array for all help command embeds
class ButtonArray(View):
    def __init__(self, ctx):
        super().__init__(timeout = 30)

        self.response = None
        self.ctx = ctx
    

    @button(label = 'ℹ️', style = nextcord.ButtonStyle.blurple)
    async def  help_info(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Send bot Info from Assets"""
        with open('Assets/HelpInfo.txt', 'r') as InfoAsset:
            Info = InfoAsset.read()
        
        embed = await Custom("Info", Info)
        await interaction.response.send_message(embed = embed, ephemeral = True)
        

    @button(label = '❌', style = nextcord.ButtonStyle.red)
    async def  dash_cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Disable all interactions"""
        for child in self.children:
            child.disabled = True  
        await self.response.edit(view = self)
        
        self.stop()


    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass

    
    async def interaction_check(self, interaction: nextcord.Interaction):
        """Make it so that only the author can use the interactions"""
        return interaction.user.id == self.ctx.author.id