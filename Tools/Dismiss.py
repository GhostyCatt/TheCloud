# Library Imports
import nextcord, json
from nextcord.ext import commands
from nextcord.ui import button, View, Select

# Custom Imports
from Functions.Embed import *

class Dismiss(View):
    """
    Dismiss
    -------
    
    Contents: 
    
    * Dismiss Button: Deletes Interaction Message
    Arguments: 
    * Context
    """
    def __init__(self, ctx:commands.Context):
        super().__init__(timeout = 30)

        self.response = None
        self.ctx = ctx
    

    @button(label = '⛔', style = nextcord.ButtonStyle.blurple)
    async def  dismiss(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()
    

    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass