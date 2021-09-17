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
    async def  onReactionAdd(self, payload:nextcord.RawReactionActionEvent):
        """Triggered when a reaction is added"""
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

        if payload.user_id == message.author.id or message.author.bot == True:
            return
        
        if message.content == None:
            content = "This message doens't have any content"
        else:
            content = message.content
            
        embed = await Custom(
            f"Starboard ⭐",
            f"{content}"
        )
        embed.add_field(name = "Author", value = message.author.mention)
        embed.add_field(name = "Starred by", value = f"<@{payload.user_id}>")
        embed.add_field(name = "Message link", value = f"Click [here](https://discord.com/channels/886521228586803210/{message.channel.id}/{message.id})")
        channel = self.bot.get_guild(886521228586803210).get_channel(Options['Channels']['Starboard'])

        await channel.send(embed = embed)

        if message.attachments:
            for attachment in message.attachments:
                await channel.send(attachment)
        

# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Starboard(bot))