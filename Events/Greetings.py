# Library Imports
import nextcord, json
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Greetings Class
class Greetings(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    
    @commands.Cog.listener('on_member_join')
    async def  GreetingsDetection(self, member:nextcord.Member):
        """Triggered when a user joins the server"""
        # Get the guild object
        Guild = self.bot.get_guild(Options['Guild']['ID'])

        # Check if the member is a bot
        if not member.bot:
            # Get all the placeholder roles and assign them
            for RoleID in Options['Roles']['PlaceHolder']:
                Role = Guild.get_role(RoleID)
                await member.add_roles(Role)
            
            # Make a welcome message
            embed = await Success(f"**{member.name}** just joined!")
            
            # Get the channel object and send the welcome messsage
            channel = Guild.get_channel(Options['Channels']['Greetings'])
            message = await channel.send(embed = embed)
            
            # Add a star reaction cuz why not :)
            await message.add_reaction('🌟')
        else:
            # Get the bot role and assign it
            Role = Guild.get_role(Options['Roles']['Bot'])
            await member.add_roles(Role)

            # Create a welcome message
            embed = await Success(f"**{member.name}** just joined!")
            
            # Get the channel object and send the welcome message
            channel = Guild.get_channel(Options['Channels']['Greetings'])
            message = await channel.send(embed = embed)

            # Add a bot reaction cuz its a bot ._.
            await message.add_reaction('🤖')

    
    @commands.Cog.listener('on_member_remove')
    async def  onMemberRemove(self, member:nextcord.Member):
        """Triggered when a user leaves the server"""
        # Get the guild object
        Guild = self.bot.get_guild(Options['Guild']['ID'])
        
        # Create a leave embed
        embed = await Fail(f"**{member.name}** left the server!")
        
        # Get the channel object and send the message
        channel = Guild.get_channel(Options['Channels']['Greetings'])  
        message = await channel.send(embed = embed)\

        # Add a star reaction
        await message.add_reaction('🌟')


# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Greetings(bot))