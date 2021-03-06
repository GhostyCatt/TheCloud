# Library Imports
from os import execl
import nextcord, json
from nextcord.ui import button, View

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Button array 
class RankView(View):
    def __init__(self, bot:commands.Bot):
        super().__init__(timeout = None)

        self.response = None
        self.bot = bot
    
    # These buttons assign roles. The roles are fetched using ID's. To modify this, change the "get_role" methods!
    @button(label = 'Bedwars', style = nextcord.ButtonStyle.blurple, custom_id = "BedwarsRankButton2000", row = 0)
    async def  bed_rank(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        Guild = self.bot.get_guild(Options['Guild']['ID'])
            
        Role = Guild.get_role(887940283570982982)
        if Role in interaction.user.roles:
            try: await interaction.user.remove_roles(Role)
            except: pass
        else:
            try: await interaction.user.add_roles(Role)
            except: pass
    

    @button(label = 'Skywars', style = nextcord.ButtonStyle.blurple, custom_id = "SkywarsRankButton2000", row = 0)
    async def  sky_rank(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        Guild = self.bot.get_guild(Options['Guild']['ID'])
            
        Role = Guild.get_role(887940393029750826)
        if Role in interaction.user.roles:
            try: await interaction.user.remove_roles(Role)
            except: pass
        else:
            try: await interaction.user.add_roles(Role)
            except: pass
    

    @button(label = 'Vanilla 1.17', style = nextcord.ButtonStyle.blurple, custom_id = "VanillaRankButton2000", row = 0)
    async def  vanilla_rank(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        Guild = self.bot.get_guild(Options['Guild']['ID'])
            
        Role = Guild.get_role(887940656423657502)
        if Role in interaction.user.roles:
            try: await interaction.user.remove_roles(Role)
            except: pass
        else:
            try: await interaction.user.add_roles(Role)
            except: pass


    @button(label = 'PvP 1.8', style = nextcord.ButtonStyle.blurple, custom_id = "PvPRankButton2000", row = 0)
    async def  pvp_rank(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        Guild = self.bot.get_guild(Options['Guild']['ID'])
            
        Role = Guild.get_role(887940767404945418)
        if Role in interaction.user.roles:
            try: await interaction.user.remove_roles(Role)
            except: pass
        else:
            try: await interaction.user.add_roles(Role)
            except: pass