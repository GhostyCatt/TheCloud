import nextcord, json
from nextcord.ext import commands
from nextcord.ui import button, View, Select

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)


# Confirm Button
class Confirm(View):
    def __init__(self, ctx):
        super().__init__(timeout = 30)

        self.ctx = ctx
    

    @button(label = '✔️', style = nextcord.ButtonStyle.green)
    async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Confirm action"""
        # Check if the person who used the button is the author
        if interaction.user.id == self.ctx.author.id:
            # Disable the buttons
            for child in self.children:
                child.disabled = True  
            
            # Stop the view and return the value
            self.stop()
            self.value = True
            
            await interaction.response.edit_message(view = self)
        else:
            await interaction.response.send_message("You don't have the permission to use that button!", ephemeral = True)


    @button(label = '❌', style = nextcord.ButtonStyle.red)
    async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """Cancel action"""
        # Check if the person who used the button is the author
        if interaction.user.id == self.ctx.author.id:
            # Disable the buttons
            for child in self.children:
                child.disabled = True  
            await interaction.response.edit_message(view = self)

            # Stop the view and return the value
            self.stop()
            self.value = False
        else:
            await interaction.response.send_message("You don't have the permission to use that button!", ephemeral = True)
    

    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass
