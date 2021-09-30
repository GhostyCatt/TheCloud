import nextcord, json
from nextcord.ext import commands
from nextcord.ui import button, View, Select

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)


# Work Button
class WorkView(View):
    def __init__(self, ctx:commands.Context):
        super().__init__(timeout = 60)

        self.ctx = ctx
        self.value = None
    

    @button(label = '1', style = nextcord.ButtonStyle.gray)
    async def one(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Check if the person who used the button is the author
        if interaction.user.id == self.ctx.author.id:
            # Disable the buttons
            for child in self.children:
                button.style = nextcord.ButtonStyle.blurple
                child.disabled = True  
            await interaction.response.edit_message(view = self)
            
            # Stop the view and return the value
            self.value = 0
            self.stop()
        else:
            await interaction.response.send_message("That button isn't for you ._.", ephemeral = True)


    @button(label = '2', style = nextcord.ButtonStyle.gray)
    async def two(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Check if the person who used the button is the author
        if interaction.user.id == self.ctx.author.id:
            # Disable the buttons
            for child in self.children:
                button.style = nextcord.ButtonStyle.blurple
                child.disabled = True  
            await interaction.response.edit_message(view = self)

            # Stop the view and return the value
            self.value = 1
            self.stop()
        else:
            await interaction.response.send_message("That button isn't for you ._.", ephemeral = True)
    

    @button(label = '3', style = nextcord.ButtonStyle.gray)
    async def three(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        # Check if the person who used the button is the author
        if interaction.user.id == self.ctx.author.id:
            # Disable the buttons
            for child in self.children:
                button.style = nextcord.ButtonStyle.blurple
                child.disabled = True  
            await interaction.response.edit_message(view = self)

            # Stop the view and return the value
            self.value = 2
            self.stop()
        else:
            await interaction.response.send_message("That button isn't for you ._.", ephemeral = True)
    

    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass
