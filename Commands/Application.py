# Library Imports
import nextcord, json
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

        await ctx.message.delete()

        if isinstance(ctx.channel, nextcord.TextChannel):
            await Fail("You can't use this command here!", ctx)
            return
            
        if ctx.channel.parent_id != Options['Channels']['Application']:
            await Fail("You can't use this command here!", ctx)
            return

        with open('Config/Application.json', 'r') as RawQuestions:
            Questions = json.load(RawQuestions)['Questions']

        await Success("Your staff application is starting, you have `2 mins` to answer all these questions, good luck!", ctx)

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

# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(StaffApp(bot))