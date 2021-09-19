# Library Imports
import nextcord, json, os, sys
from nextcord.ext import commands
from nextcord.ext.commands.flags import F

# Custom Imports
from Functions.Embed import *
from Tools.Menu import Dash
from Tools.Confirm import Confirm

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Developer Class
class Developer(commands.Cog):
    """The Developer Commands"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    

    def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.author.id in Options['Owners']


    @commands.command(name = "Dashboard", aliases = ["Dash"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  dashboard(self, ctx: commands.Context):
        """Open Developer Dashboard"""
        await ctx.channel.trigger_typing()

        await ctx.message.delete()
        embed = await Custom(
            title = f"Developer's Menu [ {ctx.author.name} ]",
            description = f"Use the buttons below to carry out bot related actions.\n\nThis dashboard will time out in `5 minutes`! Make sure you use the **Close** Button."
        )
        view = Dash(ctx)
        view.response = await ctx.send(embed = embed, view = view)

    
    @commands.command(name = "Reload", aliases = ["rl"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  reload(self, ctx: commands.Context, cog: str):
        """Reload a cog."""
        await ctx.channel.trigger_typing()

        view = Confirm(ctx)
        embed = await Custom("Confirm", f"Are you sure you want to reload `{cog}`?")
        view.response = await ctx.send(embed = embed, view = view)

        try:
            await view.wait()

            if view.value:
                cogs = self.bot.extensions

                if cog in cogs:
                    self.bot.unload_extension(cog)
                    self.bot.load_extension(cog)
                    embed = await Success(f"**`{cog}`** Has been reloaded")
                    await view.response.edit(embed = embed)

                else:
                    embed = await Fail(f"**`{cog}`** Doesn't exist.")
                    await view.response.edit(embed = embed)
            else:pass
        except:pass


    @commands.command(name = "ListCogs", aliases = ["lc"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  listcogs(self, ctx: commands.Context):
        """Get a list of active cogs."""
        await ctx.channel.trigger_typing()

        base_string = "```css\n"
        base_string += "\n- - - - - - - - - - - - - - - - -\n"
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n- - - - - - - - - - - - - - - - -```"
        
        embed = await Custom("Cogs List", base_string)
        await ctx.reply(embed = embed)


    @commands.command(name = "Load")
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  load(self, ctx: commands.Context, cog: str):
        """Load an unloaded cog."""
        await ctx.channel.trigger_typing()

        view = Confirm(ctx)
        embed = await Custom("Confirm", f"Are you sure you want to load `{cog}`?")
        view.response = await ctx.send(embed = embed, view = view)

        try:
            await view.wait()

            if view.value:
                try:
                    self.bot.load_extension(cog)
                    embed = await Success(f"**`{cog}`** Has been loaded.")
                    await view.response.edit(embed = embed)

                except commands.errors.ExtensionNotFound:
                    embed = await Fail(f"**`{cog}`** Doesn't exist")
                    await view.response.edit(embed = embed)

                except commands.errors.ExtensionAlreadyLoaded:
                    embed = await Fail(f"**`{cog}`** Was already loaded")
                    await view.response.edit(embed = embed)
            else:pass
        except:pass


    @commands.command(name = "Unload", aliases = ["ul"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  unload(self, ctx: commands.Context, cog: str):
        """Unloads a loaded cog."""
        await ctx.channel.trigger_typing()

        view = Confirm(ctx)
        embed = await Custom("Confirm", f"Are you sure you want to unload `{cog}`?")
        view.response = await ctx.send(embed = embed, view = view)

        try:
            await view.wait()

            if view.value:
                try:
                    self.bot.unload_extension(cog)
                    embed = await Success(f"**`{cog}`** Has been unloaded.")
                    await view.response.edit(embed = embed)

                except commands.errors.ExtensionNotFound:
                    embed = await Fail(f"**`{cog}`** Doesn't exist")
                    await view.response.edit(embed = embed)

                except commands.errors.ExtensionNotLoaded:
                    embed = await Fail(f"**`{cog}`** Was already unloaded")
                    await view.response.edit(embed = embed)
            else:pass
        except:pass
    

    @commands.command(name = "Shutdown")
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  shutdown(self, ctx: commands.Context):
        """Shuts the entire bots code down."""
        await ctx.channel.trigger_typing()

        view = Confirm(ctx)
        embed = await Custom("Confirm", f"Are you sure you want to shutdown?")
        view.response = await ctx.send(embed = embed, view = view)

        try:
            await view.wait()

            if view.value:
                embed = await Success(f"Bot is shutting down.")
                await view.response.edit(embed = embed)

                await self.bot.close()
            else:pass           
        except:pass


    @commands.command(name = "Restart")
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  restart(self, ctx: commands.Context):
        """Restarts the entire bot code."""
        await ctx.channel.trigger_typing()

        view = Confirm(ctx)
        embed = await Custom("Confirm", f"Are you sure you want to restart?")
        view.response = await ctx.send(embed = embed, view = view)

        try:
            await view.wait()

            if view.value:
                embed = await Success(f"Bot is restarting. Please wait a few seconds!")
                await view.response.edit(embed = embed)
                
                os.execv(sys.executable, ["python"] + sys.argv)
            else:
                pass
        except:pass
    

# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Developer(bot))