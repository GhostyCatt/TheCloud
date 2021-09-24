# Library Imports
import nextcord, json
from nextcord.ext import commands
from nextcord.ui import button, View, Select

# Custom Imports
from Functions.Embed import *

# Dismiss button
class Dismiss(View):
    def __init__(self):
        super().__init__(timeout = 30)


    @button(label = '🗑️', style = nextcord.ButtonStyle.red)
    async def  dismiss(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Delete the message
        await interaction.message.delete()
    

    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass