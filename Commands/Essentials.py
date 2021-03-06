# Library Imports
import nextcord, json
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Essentials Class
class Essentials(commands.Cog):
    """The Essential Command"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    
    @commands.command(name = "Ip", aliases = ["Connect"])
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    async def  ip(self, ctx:commands.Context):
        """Get the ip address"""
        await ctx.channel.trigger_typing()
        await Success(f"IP: `play.thecloudmc.tk`\nStatus: Under Development", ctx)
    

    @commands.command(name = "Mods", aliases = ["Modded"])
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    async def  mods(self, ctx:commands.Context):
        """Get details about how to join the modded realm"""
        await ctx.channel.trigger_typing()
        await Success(f"Coming soon!", ctx)
    

    @commands.command(name = "Vote", aliases = ["Voting"])
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    async def  vote(self, ctx:commands.Context):
        """Get the vote links"""
        await ctx.channel.trigger_typing()
        await Success(f"Coming soon!", ctx)
    

    @commands.command(name = "ETA")
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    async def  eta(self, ctx:commands.Context):
        """The rough estimate on when the server will be released"""
        await ctx.channel.trigger_typing()
        await Success(f"November 1st 2021", ctx)
    

    @commands.command(name = "Join", aliases = ["JoinGuide", "Guide"])
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    async def  join(self, ctx:commands.Context):
        """How do join our servers"""
        await ctx.channel.trigger_typing()
        await Success(f"Coming Soon", ctx)

    
    @commands.command(name = "Suggest", aliases = ["Sugg", "Rec", "Recommend"])
    @commands.cooldown(1, 3600, commands.BucketType.member)
    async def  suggest(self, ctx:commands.Context, *, suggestion:str):
        """Send a suggestion"""
        await ctx.channel.trigger_typing()
        
        # Get channel and make embed
        channel = ctx.guild.get_channel(Options['Channels']['Suggestions'])
        embed = await Custom(
            title = f"{ctx.author}'s Suggestion",
            description = suggestion
        )

        # Send embed and add reactions
        message = await channel.send(embed = embed)
        await message.add_reaction('????')
        await message.add_reaction('????')
        
        # Send success embed
        await Success(f"Your suggestion was recorded! You can suggest again in `1 hour`", ctx)

# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Essentials(bot)) 