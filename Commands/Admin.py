# Library Imports
import nextcord, json, os, sys
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *

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

        # Add a check to limit the int 1000
        if messages > 1000:
            await Fail("You can't purge more than 1000 messages!", ctx)
            return
        
        # Delete the messages
        Deleted = await ctx.channel.purge(limit = messages)

        # Send a success embed and log the process
        await Success(f"{len(Deleted)} messages were purged from {ctx.channel.mention}", ctx)
        await Log(f"`{len(Deleted)}` messages were purged from {ctx.channel.mention} by {ctx.author.mention}", ctx)
    

    @commands.group(name = 'Lockdown', aliases = ['Secure', 'Ld'])
    @commands.has_permissions(administrator = True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  lockdown(self, ctx: commands.Context):
        """Server-wide lockdown in general text channels"""
        await ctx.channel.trigger_typing()
        
        # Trigger help command if no subcommand is passed
        if ctx.subcommand_passed == None:
            await ctx.send_help(ctx.command)
        
    
    @lockdown.command(name = "Initiate", aliases = ['initiate', 'start'])
    async def  initiate(self, ctx: commands.Context):
        """Start a lockdown"""
        # For each channel in the lockdown channels list, remove the send_messages permission from members
        for item in Options['Channels']['Lockdown']:
            # Get the member role
            MemberRole = ctx.guild.get_role(Options['Roles']['Member'])
            
            # Get channel object and modify it
            Channel = ctx.guild.get_channel(item)
            await Channel.set_permissions(MemberRole, send_messages = False, read_messages = True)
        
        # Send success embed and log the process
        await Success("Lockdown has been initiated", ctx)
        await Log(f"{ctx.author.mention} Initiated lockdown", ctx)
    

    @lockdown.command(name = "Disable", aliases = ['disable', 'end'])
    async def  disable(self, ctx: commands.Context):
        """End a lockdown"""
        # For each channel in the lockdown channels list, add the send_messages permission to members
        for item in Options['Channels']['Lockdown']:
            # Get the member role
            MemberRole = ctx.guild.get_role(Options['Roles']['Member'])

            # Get the channel object to modify
            Channel = ctx.guild.get_channel(item)
            await Channel.set_permissions(
                MemberRole, send_messages = True, read_messages = True
            )
        
        # Send success embed and log the process
        await Success("Lockdown has been ended", ctx)
        await Log(f"{ctx.author.mention} Ended lockdown", ctx)
    

    @commands.command(name = "Ban", aliases = ["FuckOff"])
    @commands.has_permissions(ban_members = True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  ban(self, ctx: commands.Context, user: nextcord.Member, reason: str = "The ban hammer has spoken!"):
        """Ban users from the server"""
        await ctx.channel.trigger_typing()

        # Check if the user is tryin to ban themselves
        if user == ctx.author:
            await Fail("You can't ban yourself...", ctx)
            return
        
        # Ban the user with reason
        await ctx.guild.ban(user, reason = reason)

        # Send success embed and log the process
        await Success(f"{user} was banned by {ctx.author.mention}")
        await Log(f"`{user}` was banned by {ctx.author.mention} for `{reason}`", ctx)
    

    @commands.command(name = "Unban", aliases = ["FuckBack"])
    @commands.has_permissions(ban_members = True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  unban(self, ctx: commands.Context, user:str):
        """Unban users from the server"""
        await ctx.channel.trigger_typing()

        # Get a list of currently banned members
        Bans = await ctx.guild.bans()
        try:
            # Split the user to name and discriminator
            MemberName, MemberDiscriminator = user.split("#")
        except:
            await Fail("You haven't entered the user properly, use the format `User#Discriminator`", ctx)
            return

        # For every ban on the guild, check if it matches the user entered
        count = 0
        for Entry in Bans:
            user = Entry.user

            if (user.name, user.discriminator) == (MemberName, MemberDiscriminator):
                await ctx.guild.unban(user)
                await Success(f"{user} was successfully unbanned from the server!")

                await Log(f"`{user}` was unbanned by {ctx.author.mention}", ctx)
                count += 1

        # If count hasn't changed, send a fail embed saying the user wasn't banned.
        if count == 0:
            await Fail(f"I don't think {user} is banned...", ctx)


    @commands.command(name = "Kick", aliases = ["Gtfo"])
    @commands.has_permissions(ban_members = True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  kick(self, ctx: commands.Context, user: nextcord.Member, reason: str = "Kicked by admins!"):
        """Kick users from the server"""
        await ctx.channel.trigger_typing()

        # Check if user is trying to kick themselves
        if user == ctx.author:
            await Fail("You can't kick yourself...", ctx)
            return
        
        # Kick the user with a reson
        await ctx.guild.kick(user, reason = reason)

        # Send success embed and log the process
        await Success(f"{user} was kicked by {ctx.author.mention}")
        await Log(f"`{user}` was kicked by {ctx.author.mention} for `{reason}`", ctx)


    @commands.command(name = "Rules", aliases = ["Rule"])
    @commands.has_permissions(manage_messages = True)
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  rules(self, ctx: commands.Context, *, keyword: str = None):
        """Get text from the rules"""
        await ctx.channel.trigger_typing()

        # Check if no keyword was passed, if so, send all the rules
        if keyword == None:
            with open('Assets/Rules.txt', 'r', encoding = 'utf-8') as RulesFile:
                content = RulesFile.read()
                sections = content.split("━━━━━━━━━━━━━━━━━━━━")
                for section in sections:
                    embed = nextcord.Embed(description = section, color = nextcord.Colour.blurple())
                    await ctx.send(embed = embed)
                return
        
        # Open the rules file and get a list of lines that matched
        with open('Assets/Rules.txt', 'r', encoding = 'utf-8') as RulesFile:
            match = []
            for line in RulesFile:
                if keyword in line:
                    if line.startswith(("━", "**₊")): pass
                    else: match.append(line)
        
        # If no lines matched the search criteria, send fail embed
        if match == []:
            await Fail(f"I couldn't find anything with `{keyword}`", ctx)
            return
        
        # Create a single string with all the matched lines
        desc = ''
        for line in match:
            desc += f"{line}"

        # Send the success embed with all the rules
        await Success(desc, ctx)


# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Admin(bot))