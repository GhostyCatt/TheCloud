# Library Imports
import nextcord, json
from nextcord.ui import button, View, Select

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Self Role Drowdowns
class AgeMenu(Select):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        options = [
            nextcord.SelectOption(label = "- 13", description = "Click to get this role", value = "886537316418609172"),
            nextcord.SelectOption(label = "+ 13", description = "Click to get this role", value = "886537379450589215"),
            nextcord.SelectOption(label = "+ 16", description = "Click to get this role", value = "886537464452366376"),
            nextcord.SelectOption(label = "+ 18", description = "Click to get this role", value = "886537714206392320"),
            nextcord.SelectOption(label = "None", description = "Click to remove all age roles", value = "000000")
        ]

        super().__init__(placeholder = 'Age Roles', min_values = 1, max_values = 1, options = options, custom_id = "AgeRoleMenu2000")


    async def callback(self, interaction: nextcord.Interaction):
        try:
            Guild = self.bot.get_guild(886521228586803210)
            AgeRole = Guild.get_role(int(self.values[0]))

            AgeRoles = [
                886537316418609172, 886537379450589215, 886537464452366376, 886537714206392320
            ]


            for Role in AgeRoles:
                Role = Guild.get_role(Role)
                await interaction.user.remove_roles(Role)

            if self.values[0] == "000000":
                return

            await interaction.user.add_roles(AgeRole)
        except: pass


class SexMenu(Select):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        options = [
            nextcord.SelectOption(label = "Male", description = "Click to get this role", value = "886537847258112071"),
            nextcord.SelectOption(label = "Female", description = "Click to get this role", value = "886537907412815912"),
            nextcord.SelectOption(label = "None", description = "Click to remove all gender roles", value = "000000")
        ]

        super().__init__(placeholder = 'Gender Roles', min_values = 1, max_values = 1, options = options, custom_id = "SexRoleMenu2000")


    async def callback(self, interaction: nextcord.Interaction):
        try:
            Guild = self.bot.get_guild(886521228586803210)
            GenderRole = Guild.get_role(int(self.values[0]))

            GenderRoles = [
                886537847258112071, 886537907412815912
            ]


            for Role in GenderRoles:
                Role = Guild.get_role(Role)
                await interaction.user.remove_roles(Role)

            if self.values[0] == "000000":
                return

            await interaction.user.add_roles(GenderRole)
        except: pass


class InterestMenu(Select):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        options = [
            nextcord.SelectOption(label = "Arts", description = "Click to get this role", value = "886538932018348032"),
            nextcord.SelectOption(label = "Sports", description = "Click to get this role", value = "886538985852248094"),
            nextcord.SelectOption(label = "Music", description = "Click to get this role", value = "886539050062864404"),
            nextcord.SelectOption(label = "Reading", description = "Click to get this role", value = "886539142740209714"),
            nextcord.SelectOption(label = "Cooking", description = "Click to get this role", value = "886539267998896128"),
            nextcord.SelectOption(label = "Singing", description = "Click to get this role", value = "886539873631211520"),
            nextcord.SelectOption(label = "None", description = "Click to remove all gender roles", value = "000000")
        ]

        super().__init__(placeholder = 'Interest Roles', min_values = 1, max_values = 6, options = options, custom_id = "InterestRoleMenu2000")


    async def callback(self, interaction: nextcord.Interaction):
        try:
            Guild = self.bot.get_guild(886521228586803210)
            
            InterestRoles = [
                886538932018348032, 886538985852248094, 886539050062864404, 886539142740209714, 886539267998896128, 886539873631211520
            ]
            for Role in InterestRoles:
                Assign = Guild.get_role(Role)
                await interaction.user.remove_roles(Assign)
            
            if "000000" in self.values:
                return
            
            else:
                for Role in self.values:
                    Assign = Guild.get_role(Role)
                    await interaction.user.add_roles(Assign)
        except: pass


# Button array 
class RoleView(View):
    def __init__(self, bot:commands.Bot):
        super().__init__(timeout = None)

        self.response = None
        
        self.add_item(AgeMenu(bot))
        self.add_item(SexMenu(bot))
        self.add_item(InterestMenu(bot))