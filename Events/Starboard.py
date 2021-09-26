# Library Imports
import nextcord, json
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Starboard Class
class Starboard(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    
    @commands.Cog.listener('on_raw_reaction_add')
    async def  StarboardDetection(self, payload:nextcord.RawReactionActionEvent):
        """Triggered when a reaction is added"""
        # Return if the reaction isn't a star
        if not payload.emoji.name in ["⭐"]:
            return

        # Get the message object
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

        # Return if a bots message is being starred, or if the author is starring their own message
        if payload.user_id == message.author.id or message.author.bot == True:
            return
        
        # Return if the message is already starred twice
        reaction = nextcord.utils.get(message.reactions, emoji = payload.emoji.name)
        if reaction and reaction.count > 2:
            return
        
        # If theres no content in the message, sent a default
        if message.content == None:
            content = "**This message didn't have any content**"
        else:
            content = message.content
        
        # Start creating the embed
        embed = await Custom(
            f"{message.author} {payload.emoji.name}",
            f"{content}\n\n**[Click here to go the the message](https://discord.com/channels/{Options['Guild']['ID']}/{message.channel.id}/{message.id})**"
        )
        embed.add_field(name = "Starred by", value = f"<@{payload.user_id}>", inline = False)

        # Get the channel object and send the embed
        channel = self.bot.get_guild(Options['Guild']['ID']).get_channel(Options['Channels']['Starboard'])
        await channel.send(embed = embed)

        # If the message had any attachments, send them too
        if message.attachments:
            for attachment in message.attachments:
                await channel.send(attachment)
        

# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Starboard(bot))