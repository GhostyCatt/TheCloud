# Library Imports
import nextcord, json
from nextcord.ui import button, View, Select

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Help Dropdown
class Dropdown(Select):
    def __init__(self, help, options):  
        self.helpcommand = help  
        super().__init__(placeholder = 'Select a module here...', min_values = 1, max_values = 1, options = options, row = 0)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "Home": embed = await self.helpcommand.get_help_embed(self.helpcommand.get_bot_mapping())
        else: embed = await self.helpcommand.get_cog_help_embed(self.helpcommand.context.bot.get_cog(self.values[0]))
        await interaction.response.edit_message(embed = embed)
    

class HelpView(View):
    def __init__(self, help, options):
        super().__init__(timeout = 30)
        self.helpcommand = help

        self.response = None
        
        self.add_item(nextcord.ui.Button(label = "Website", url = Options['Website'], row = 1))
        self.add_item(nextcord.ui.Button(label = "Info", url = "https://discord.com/channels/886521228586803210/886547284815409173/", row = 1))
        self.add_item(Dropdown(help, options))
    
    @button(label = 'Dismiss', style = nextcord.ButtonStyle.red, row = 1)
    async def  dismiss(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()
    
    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass
    
    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        return interaction.user.id == self.helpcommand.context.author.id