# Library Imports
import nextcord, json
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *
from Tools.Roles import RoleView

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Roles Class
class Roles(commands.Cog):
    """The Self Roles Commands"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    
    @commands.command(name = "RoleMenu")
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    @commands.has_role(Options['Roles']['Owner'])
    async def  rolemenu(self, ctx:commands.Context):
        """Send the Self Roles Menu"""
        await ctx.channel.trigger_typing()
        
        # Create embed
        embed = await Custom("Self Roles", f"Use the dropdowns below to get/remove roles from yourself, or click the buttons to clear all your profile roles!")
        embed.set_footer(text = "Note: If the bot is offline, this buttons won't respond.")
        
        # Send message with counter
        view = RoleView(self.bot)
        view.response = await ctx.send("Self Roles", embed = embed, view = view)


# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Roles(bot))