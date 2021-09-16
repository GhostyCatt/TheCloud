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

# Admin Class
class Admin(commands.Cog):
    """The Admin Commands"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "Purge", aliases = ["ClearChat"])
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  purge(self, ctx: commands.Context, messages: int = 100):
        """Delete some messages from the current channel"""
        await ctx.channel.trigger_typing()
        if messages > 1000:
            await Fail("You can't purge more than 1000 messages!", ctx)
            return
        
        await ctx.channel.purge(limit = messages)
        await Success(f"{messages} messages were purged from {ctx.channel.mention}", ctx)

        await Log(f"`{messages}` messages were purged from {ctx.channel.mention} by {ctx.author.mention}", ctx)
    

    @commands.group(name = 'Lockdown', aliases = ['Secure', 'Ld'])
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  lockdown(self, ctx: commands.Context):
        """Server-wide lockdown in general text channels"""
        await ctx.channel.trigger_typing()
        
        if ctx.subcommand_passed == None:
            await ctx.send_help(ctx.command)
        
    
    @lockdown.command(name = "Initiate", aliases = ['initiate', 'start'])
    async def  initiate(self, ctx: commands.Context):
        """Start a lockdown"""
        for item in Options['Channels']['Lockdown']:
            MemberRole = ctx.guild.get_role(Options['Roles']['Member'])
            Channel = ctx.guild.get_channel(item)
            await Channel.set_permissions(
                MemberRole, send_messages = False, read_messages = True
            )
        
        await Success("Lockdown has been initiated", ctx)

        await Log(f"{ctx.author.mention} Initiated lockdown", ctx)
    

    @lockdown.command(name = "Disable", aliases = ['disable', 'end'])
    async def  disable(self, ctx: commands.Context):
        """End a lockdown"""
        for item in Options['Channels']['Lockdown']:
            MemberRole = ctx.guild.get_role(Options['Roles']['Member'])
            Channel = ctx.guild.get_channel(item)
            await Channel.set_permissions(
                MemberRole, send_messages = True, read_messages = True
            )
        
        await Success("Lockdown has been ended", ctx)

        await Log(f"{ctx.author.mention} Ended lockdown", ctx)
    

    @commands.command(name = "Ban", aliases = ["FuckOff"])
    @commands.has_permissions(ban_members = True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  ban(self, ctx: commands.Context, user: nextcord.Member, reason: str = "The ban hammer has spoken!"):
        """Ban users from the server"""
        await ctx.channel.trigger_typing()

        if user == ctx.author:
            await Fail("You can't ban yourself...", ctx)
            return
        
        await ctx.guild.ban(user, reason = reason)
        await Success(f"{user} was banned by {ctx.author.mention}")

        await Log(f"`{user}` was banned by {ctx.author.mention} for `{reason}`", ctx)
    

    @commands.command(name = "Unban", aliases = ["FuckBack"])
    @commands.has_permissions(ban_members = True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  unban(self, ctx: commands.Context, user:str):
        """Unban users from the server"""
        await ctx.channel.trigger_typing()

        Bans = await ctx.guild.bans()
        try:
            MemberName, MemberDiscriminator = user.split("#")
        except:
            await Fail("You haven't entered the user properly, use the format `User#Discriminator`", ctx)
            return

        count = 0
        for Entry in Bans:
            user = Entry.banned_users

            if (user.name, user.discriminator) == (MemberName, MemberDiscriminator):
                await ctx.guild.unban(user)
                await Success(f"{user} was successfully unbanned from the server!")

                await Log(f"`{user}` was unbanned by {ctx.author.mention}", ctx)
                count += 1

        if count == 0:
            await Fail(f"I don't think {user} is banned...", ctx)


    @commands.command(name = "Kick", aliases = ["Gtfo"])
    @commands.has_permissions(ban_members = True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  kick(self, ctx: commands.Context, user: nextcord.Member, reason: str = "Kicked by admins!"):
        """Kick users from the server"""
        await ctx.channel.trigger_typing()

        if user == ctx.author:
            await Fail("You can't kick yourself...", ctx)
            return
        
        await ctx.guild.ban(user, reason = reason)
        await Success(f"{user} was kicked by {ctx.author.mention}")

        await Log(f"`{user}` was kicked by {ctx.author.mention} for `{reason}`", ctx)


    @commands.command(name = "Rules", aliases = ["Rule"])
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  rules(self, ctx: commands.Context, *, keyword: str = None):
        """Get text from the rules"""
        await ctx.channel.trigger_typing()

        if keyword == None:
            with open('Assets/Rules.txt', 'r', encoding = 'utf-8') as RulesFile:
                content = RulesFile.read()
                await Success(content, ctx)
                return
        
        with open('Assets/Rules.txt', 'r', encoding = 'utf-8') as RulesFile:
            match = [line for line in RulesFile if keyword in line]
        
        if match == []:
            await Fail(f"I couldn't find anything with `{keyword}`", ctx)
            return
            
        desc = ''
        for line in match:
            desc += f"{line}"

        await Success(desc, ctx)


# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Admin(bot))