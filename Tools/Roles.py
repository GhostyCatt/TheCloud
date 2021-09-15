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
            nextcord.SelectOption(label = "- 13", description = "Click to get/remove this role", value = "886537316418609172"),
            nextcord.SelectOption(label = "+ 13", description = "Click to get/remove this role", value = "886537379450589215"),
            nextcord.SelectOption(label = "+ 16", description = "Click to get/remove this role", value = "886537464452366376"),
            nextcord.SelectOption(label = "+ 18", description = "Click to get/remove this role", value = "886537714206392320"),
        ]

        super().__init__(placeholder = 'Age Roles', min_values = 1, max_values = 1, options = options, custom_id = "AgeRoleMenu2000", row = 3)


    async def callback(self, interaction: nextcord.Interaction):
        try:
            Guild = self.bot.get_guild(886521228586803210)
            Role = Guild.get_role(int(self.values[0]))

            if Role in interaction.user.roles:
                await interaction.user.remove_roles(Role)

            else:
                await interaction.user.add_roles(Role)
        except: pass

        await interaction.response.edit_message(embed = interaction.message.embeds[0])


class SexMenu(Select):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        options = [
            nextcord.SelectOption(label = "Male", description = "Click to get/remove this role", value = "886537847258112071"),
            nextcord.SelectOption(label = "Female", description = "Click to get/remove this role", value = "886537907412815912"),
        ]

        super().__init__(placeholder = 'Gender Roles', min_values = 1, max_values = 1, options = options, custom_id = "SexRoleMenu2000", row = 2)


    async def callback(self, interaction: nextcord.Interaction):
        try:
            Guild = self.bot.get_guild(886521228586803210)
            Role = Guild.get_role(int(self.values[0]))

            if Role in interaction.user.roles:
                await interaction.user.remove_roles(Role)

            else:
                await interaction.user.add_roles(Role)
        except: pass

        await interaction.response.edit_message(embed = interaction.message.embeds[0])


class InterestMenu(Select):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        options = [
            nextcord.SelectOption(label = "Arts", description = "Click to get/remove this role", value = "886538932018348032"),
            nextcord.SelectOption(label = "Sports", description = "Click to get/remove this role", value = "886538985852248094"),
            nextcord.SelectOption(label = "Music", description = "Click to get/remove this role", value = "886539050062864404"),
            nextcord.SelectOption(label = "Reading", description = "Click to get/remove this role", value = "886539142740209714"),
            nextcord.SelectOption(label = "Cooking", description = "Click to get/remove this role", value = "886539267998896128"),
            nextcord.SelectOption(label = "Singing", description = "Click to get/remove this role", value = "886539873631211520"),
        ]

        super().__init__(placeholder = 'Interest Roles', min_values = 1, max_values = 1, options = options, custom_id = "InterestRoleMenu2000", row = 1)


    async def callback(self, interaction: nextcord.Interaction):
        try:
            Guild = self.bot.get_guild(886521228586803210)
            Role = Guild.get_role(int(self.values[0]))

            if Role in interaction.user.roles:
                await interaction.user.remove_roles(Role)

            else:
                await interaction.user.add_roles(Role)
        except: pass

        await interaction.response.edit_message(embed = interaction.message.embeds[0])


class PingMenu(Select):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        options = [
            nextcord.SelectOption(label = "Announcement", description = "Click to get/remove this role", value = "886540581004795904"),
            nextcord.SelectOption(label = "Event", description = "Click to get/remove this role", value = "886540636168282132"),
            nextcord.SelectOption(label = "Partner", description = "Click to get/remove this role", value = "886540681663873065"),
            nextcord.SelectOption(label = "Chat Revive", description = "Click to get/remove this role", value = "886540760583901185")
        ]

        super().__init__(placeholder = 'Mention Roles', min_values = 1, max_values = 1, options = options, custom_id = "PingRoleMenu2000", row = 0)


    async def callback(self, interaction: nextcord.Interaction):
        try:
            Guild = self.bot.get_guild(886521228586803210)
            Role = Guild.get_role(int(self.values[0]))

            if Role in interaction.user.roles:
                await interaction.user.remove_roles(Role)

            else:
                await interaction.user.add_roles(Role)
        except: pass

        await interaction.response.edit_message(embed = interaction.message.embeds[0])


# Button array 
class RoleView(View):
    def __init__(self, bot:commands.Bot):
        super().__init__(timeout = None)

        self.response = None
        self.bot = bot
        
        self.add_item(AgeMenu(bot))
        self.add_item(SexMenu(bot))
        self.add_item(InterestMenu(bot))
        self.add_item(PingMenu(bot))
    

    @button(label = 'Clear Roles', style = nextcord.ButtonStyle.red, custom_id = "ClearRoleButton2000", row = 4)
    async def  clear(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        Guild = self.bot.get_guild(886521228586803210)

        RoleIDS = [
            886537316418609172, 886537379450589215, 886537464452366376, 886537714206392320,
            886537847258112071, 886537907412815912,
            886538932018348032, 886538985852248094, 886539050062864404, 886539142740209714, 886539267998896128, 886539873631211520,
            886540581004795904, 886540636168282132, 886540681663873065, 886540760583901185
        ]

        try:
            for RoleID in RoleIDS:
                Role = Guild.get_role(RoleID)
                if Role in interaction.user.roles:
                    await interaction.user.remove_roles(Role)
        except: pass