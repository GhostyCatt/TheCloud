# Library Imports
import nextcord, json, asyncio
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *
from Tools.Support import *
from Tools.Question import QuestionView

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Staffapp Class
class StaffApp(commands.Cog):
    """The staffapp Commands"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    
    @commands.command(name = "ApplicationMenu")
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    @commands.has_role(Options['Roles']['Owner'])
    async def  applicationmenu(self, ctx:commands.Context):
        """Send the StaffApp Menu"""
        await ctx.channel.trigger_typing()
        
        # Create embed
        embed = await Custom("Staff Application", f"Click the button below to open a new staff app!\n\nUse the command `{Options['Prefix']}apply` in the thread to start your staff application!")
        embed.set_footer(text = "Note: If the bot is offline, this button won't respond.")
        
        # Send message with counter
        view = StaffAppView(self.bot)
        view.response = await ctx.send(embed = embed, view = view)

    
    @commands.command(name = "Apply")
    @commands.cooldown(1, Options['Cooldown'], commands.BucketType.member)
    async def  apply(self, ctx:commands.Context):
        """Start a staff application"""
        await ctx.channel.trigger_typing()

        # Return of the command is used in a normal text channel
        if isinstance(ctx.channel, nextcord.TextChannel):
            await Fail("You can't use this command here!", ctx)
            return
        
        # Return if the parent channel isn't the staffapp channel
        if ctx.channel.parent_id != Options['Channels']['Application']:
            await Fail("You can't use this command here!", ctx)
            return

        # Open the questions file and convert it to json
        with open('Config/Application.json', 'r') as RawQuestions:
            Questions = json.load(RawQuestions)['Questions']

        # Send a success embed
        await Success("Your staff application is starting in 5 seconds, you will have `5 mins` to answer all these questions, good luck!\n\nPlease take this seriously and DO NOT make troll / prank applications. We WILL ban you for this.", ctx)

        # Wait for 5 seconds
        await asyncio.sleep(5)

        # Send all the questions with a select menu under them
        for Question in Questions:
            embed = await Custom(
                Question["Name"],
                Question["Description"]
            )

            MenuOptions = []
            for option in Question['Options']:
                MenuOptions.append(
                    nextcord.SelectOption(label = option['Name'], description = option['Description'])
                )
            
            view = QuestionView(ctx, MenuOptions)

            await ctx.send(embed = embed, view = view)
        
        # Send a final message
        await Success("You can leave the thread after answering all these questions! Owner / Coowners will check out your application and get back to you when they can.", ctx)

# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(StaffApp(bot))