# Library Imports
import nextcord, json
from nextcord.ui import button, View, Select

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Dropdown Menu for main help command
class Dropdown(Select):
    def __init__(self, ctx:commands.Context, options):
        self.ctx = ctx

        # Super init
        super().__init__(placeholder = 'Select your answer here...', min_values = 1, max_values = 1, options = options)


    async def callback(self, interaction: nextcord.Interaction):
        """Module Specific Help"""

        if self.values[0] != "Other":
            await interaction.response.edit_message(content = self.values[0], view = None)
        else:
            await interaction.response.edit_message(content = "Not specified.", view = None)



# Button array for the main help command embed
class QuestionView(View):
    def __init__(self, ctx, options:list):
        super().__init__(timeout = 60)

        self.response = None
        self.ctx = ctx
        
        self.add_item(Dropdown(self.ctx, options))

    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass