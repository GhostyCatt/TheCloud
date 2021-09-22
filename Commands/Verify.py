# Library Imports
import nextcord, json
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *
from Tools.Verify import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Verify Class
class Verify(commands.Cog):
    """The Verify Command"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    
    @commands.command(name = "Verify")
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    @commands.has_role(Options['Roles']['Owner'])
    async def  verify(self, ctx:commands.Context):
        """Send the Verification Menu"""
        await ctx.channel.trigger_typing()
        
        # Create embed
        embed = await Custom("Verify", "Click on the button below to gain access to the rest of the server!\n\nMake sure you have read the rules before doing so.")
        embed.set_footer(text = "Note: If the bot is offline, this button won't respond.")
        
        # Send message with the verify button
        view = VerifyView(self.bot)
        view.response = await ctx.send(embed = embed, view = view)
    

# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Verify(bot))