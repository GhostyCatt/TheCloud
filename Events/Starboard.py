# Library Imports
import nextcord, json
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Starboard Class
class Starboard(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    
    @commands.Cog.listener('on_raw_reaction_add')
    async def  onReactionAdd(self, payload:nextcord.RawReactionActionEvent):
        """Triggered when a reaction is added"""
        
        


# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Starboard(bot))