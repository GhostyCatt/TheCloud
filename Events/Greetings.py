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
    async def  onMemberJoin(self, member:nextcord.Member):
        """Triggered when a user joins the server"""
        Guild = self.bot.get_guild(886521228586803210)

        if not member.bot:
            for RoleID in Options['Roles']['PlaceHolder']:
                Role = Guild.get_role(RoleID)
                await member.add_roles(Role)
            
            embed = await Success(f"**{member.name}** just joined!")
            
            channel = Guild.get_channel(886559028136792084)
            message = await channel.send(embed = embed)
            await message.add_reaction('🌟')
        else:
            Role = Guild.get_role(Options['Roles']['Bot'])
            await member.add_roles(Role)

            embed = await Success(f"**{member.name}** just joined!")
            
            channel = Guild.get_channel(886559028136792084)
            message = await channel.send(embed = embed)
            await message.add_reaction('🤖')

    
    @commands.Cog.listener('on_member_remove')
    async def  onMemberRemove(self, member:nextcord.Member):
        """Triggered when a user leaves the server"""
        Guild = self.bot.get_guild(886521228586803210)
            
        embed = await Fail(f"**{member.name}** left the server!")
            
        channel = Guild.get_channel(886559028136792084)  
        message = await channel.send(embed = embed)
        await message.add_reaction('🌟')


# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Greetings(bot))