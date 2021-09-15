# Library Imports
import nextcord, json
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *
from Tools.Support import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Support Class
class Support(commands.Cog):
    """The Support Commands"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    
    @commands.command(name = "TicketMenu")
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    @commands.has_role(Options['Roles']['Owner'])
    async def  ticketmenu(self, ctx:commands.Context):
        """Send the Ticket Menu"""
        await ctx.channel.trigger_typing()
        
        # Create embed
        embed = await Custom("Support", "Click the button below to open a new ticket!\n\nYou **MUST** have a legitimate reason to create the ticket, or you may be kicked or banned from the server.")
        embed.set_footer(text = "Note: If the bot is offline, this button won't respond.")
        
        # Send message with counter
        view = SupportView(self.bot)
        view.response = await ctx.send(embed = embed, view = view)
    

    @commands.command(name = "IngameMenu")
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    @commands.has_role(Options['Roles']['Owner'])
    async def  ingamemenu(self, ctx:commands.Context):
        """Send the Ingame Help Menu"""
        await ctx.channel.trigger_typing()
        
        # Create embed
        embed = await Custom("Ingame Help", "Click the button below to open a new ticket!\n\nYou **MUST** have a legitimate reason to create the ticket, or you may be kicked or banned from the server.")
        embed.set_footer(text = "Note: If the bot is offline, this button won't respond.")
        
        # Send message with counter
        view = SupportView(self.bot)
        view.response = await ctx.send(embed = embed, view = view)
    

    @commands.command(name = "ReportMenu")
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    @commands.has_role(Options['Roles']['Owner'])
    async def  reportmenu(self, ctx:commands.Context):
        """Send the Report Menu"""
        await ctx.channel.trigger_typing()
        
        # Create embed
        embed = await Custom("Player Report", f"Click the button below to open a new report!\n\nMake sure you have screenshots and/or any required evidence against the player you are reporting.")
        embed.set_footer(text = "Note: If the bot is offline, this button won't respond.")
        
        # Send message with counter
        view = SupportView(self.bot)
        view.response = await ctx.send(embed = embed, view = view)

    
    @commands.command(name = "Close")
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    @commands.has_role(Options['Roles']['Helper'])
    async def  close(self, ctx:commands.Context):
        """Close Thread"""
        SupportChannels = [
            886566990788034610,
            886569978940260353,
            886567102683693126,
            886567334381240330
        ]
        if isinstance(ctx.channel, nextcord.Thread):
            if ctx.channel.parent_id in SupportChannels:
                await ctx.channel.delete()
            else:
                await Fail("This command can only be used in support channel threads", ctx)
                print("in")
        else:
            await Fail("This command can only be used in support channel threads", ctx)


# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Support(bot))