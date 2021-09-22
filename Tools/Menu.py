import nextcord, json, os, sys
from nextcord.ext import commands
from nextcord.ui import button, View, Select

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Dashboard view
class Dash(View):
    def __init__(self, ctx:commands.Context):
        super().__init__(timeout = 300)

        self.response = None
        self.ctx = ctx

    
    # These functions carry out the same action used in Commands/Developer.py
    @button(label = 'Restart', style = nextcord.ButtonStyle.blurple)
    async def  restart(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await Success("Bot is restarting!", self.ctx)
            await self.response.delete()
            os.execv(sys.executable, ["python"] + sys.argv)
        else:
            await interaction.response.send_message("You don't have the permission to use that button!", ephemeral = True)
    

    @button(label = 'Shutdown', style = nextcord.ButtonStyle.blurple)
    async def  shutdown(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await Success("Bot is shutting down!", self.ctx)
            await self.response.delete()
            await self.ctx.bot.close()
        else:
            await interaction.response.send_message("You don't have the permission to use that button!", ephemeral = True)

    
    @button(label = 'List Cogs', style = nextcord.ButtonStyle.blurple)
    async def  cogs(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            base_string = "```css\n"
            base_string += "\n- - - - - - - - - - - - - - - - -\n"
            base_string += "\n".join([str(cog) for cog in self.ctx.bot.extensions])
            base_string += "\n- - - - - - - - - - - - - - - - -```"
            
            embed = await Custom("Cogs List", base_string)

            await interaction.response.send_message(embed = embed, ephemeral = True)

            await self.response.delete()
        else:
            await interaction.response.send_message("You don't have the permission to use that button!", ephemeral = True)
    

    @button(label = '🗑️', style = nextcord.ButtonStyle.red)
    async def  close(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user.id == self.ctx.author.id:
            await self.response.delete()
        else:
            await interaction.response.send_message("You don't have the permission to use that button!", ephemeral = True)

    async def on_timeout(self):
        """Disable all interactions on timeout"""
        try:
            for child in self.children:
                child.disabled = True  
            await self.response.edit(view = self)
        except: pass
