# Library Imports
import nextcord, json
from nextcord.ext import commands
from nextcord.ui import button, View, Select

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Support Class
class SupportView(View):
    def __init__(self, bot:commands.Bot):
        super().__init__(timeout = None)

        self.response = None
        self.bot = bot
    

    @button(label = '🎫 New', style = nextcord.ButtonStyle.blurple, custom_id = "TicketButton2000")
    async def  new(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        Message = await interaction.channel.send("Creating Thread...")
        Thread = await interaction.channel.create_thread(
            name = f"{interaction.user.name}{interaction.user.discriminator}",
            message = Message
        )
        
        try:
            await Thread.add_user(interaction.user)
            await Message.delete()

            Guild = self.bot.get_guild(Options['Guild']['ID'])
            HelperRole = Guild.get_role(Options['Roles']['Helper'])

            embed = await Custom(f"{interaction.user.name}'s Thread", f"Welcome to your thread, any user can join this thread. Use the command `{Options['Prefix']}close` to close this thread.")
            await Thread.send(
                content = HelperRole.mention,
                embed = embed
            )
        except: pass


# Staff App Class
class StaffAppView(View):
    def __init__(self, bot:commands.Bot):
        super().__init__(timeout = None)

        self.response = None
        self.bot = bot
    

    @button(label = '📜 Apply', style = nextcord.ButtonStyle.blurple, custom_id = "StaffButton2000")
    async def  new(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        Message = await interaction.channel.send("Creating Thread...")
        Thread = await interaction.channel.create_thread(
            name = f"{interaction.user.name}{interaction.user.discriminator}",
            message = Message
        )
        
        await Thread.add_user(interaction.user)
        await Message.delete()

        try:
            embed = await Custom(f"{interaction.user.name}'s Staff App", f"This is your staff application. Use the `{Options['Prefix']}apply` command to start!")
            await Thread.send(embed = embed)
        except: pass