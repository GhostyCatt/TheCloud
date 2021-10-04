# Library Imports
import nextcord, json
from nextcord.ext import commands
from nextcord.ui import button, View, Select

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Verify Class
class VerifyView(View):
    def __init__(self, bot:commands.Bot):
        super().__init__(timeout = None)

        self.response = None
        self.bot = bot
    

    @button(label = '✔️', style = nextcord.ButtonStyle.green, custom_id = "VerificationButton2000")
    async def  verify(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        Guild = self.bot.get_guild(Options['Guild']['ID'])
        MemberRole = Guild.get_role(Options['Roles']['Member'])
        MutedRole = Guild.get_role(Options['Roles']['Muted'])

        if MemberRole in interaction.user.roles:
            embed = await Fail("You have already verified!")
            await interaction.response.send_message(embed = embed, ephemeral = True)
            return
        elif MutedRole in interaction.user.roles:
            embed = await Fail("You're muted! You can't verify!")
            await interaction.response.send_message(embed = embed, ephemeral = True)
            return
        
        await interaction.user.add_roles(MemberRole)

        embed = await Success("You now have access to the rest of the server!")

        # Send the confirmation message
        await interaction.response.send_message(embed = embed, ephemeral = True)