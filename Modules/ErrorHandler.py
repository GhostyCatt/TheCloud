# Library Imports
import nextcord, traceback, sys, pymongo
from nextcord.ext import commands
from nextcord.ui import View, button

# Custom Imports
from Functions.Embed import *
from Views.Dismiss import Dismiss

# Error Handler Class
class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener('on_command_error')
    async def ErrorListener(self, ctx:commands.Context, error):
        """
        ErrorListener
        ------------
        Listens for any error that takes place while trying to run any command.
        """
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound)
        error = getattr(error, 'original', error)
        
        # Ignore error if needed
        if isinstance(error, ignored):
            return

        # Trigger if command used is disabled
        if isinstance(error, commands.DisabledCommand):
            embed = await Fail(f'{ctx.command} has been disabled.')
            await ctx.reply(embed = embed, mention_author = False)
        
        # Trigger if command used is on cooldown
        elif isinstance(error, commands.CommandOnCooldown):
            embed = await Fail(f'{ctx.command} is on cooldown. `{round(error.retry_after)}`')
            await ctx.reply(embed = embed, mention_author = False)
        
        # Trigger if author doens't meet permissions threshold
        elif isinstance(error, commands.MissingPermissions):
            embed = await Fail(f'You don\'t have the permissions to run {ctx.command}')
            await ctx.reply(embed = embed, mention_author = False)
        
        # Trigger if bot doesn't have the permissions needed to carry out a command
        elif isinstance(error, commands.BotMissingPermissions):
            embed = await Fail(f'I don\'t have enough permissions to handle the {ctx.command} command.')
            await ctx.reply(embed = embed, mention_author = False)

        # Trigger if use doesn't have the required role to run a command
        elif isinstance(error, commands.MissingRole):
            embed = await Fail(f'You don\'t have the role required to run the {ctx.command} command.')
            await ctx.reply(embed = embed, mention_author = False)
        
        # Trigger if command can't be used in dms
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except nextcord.HTTPException:
                pass
        
        # Trigger if any arguments are missing
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)

        # Trigger if member not found
        elif isinstance(error, commands.MemberNotFound):
            embed = await Fail(error)
            await ctx.reply(embed = embed, mention_author = False)
            
        # General error
        else:
            embed = await Fail(f'Something went wrong in the command {ctx.command}')
            await ctx.reply(embed = embed, mention_author = False)

            print('Ignoring exception in command {}:'.format(ctx.command), file = sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)


# Add error handler to the bot
def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))