# Library Imports
import nextcord, json
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# onMessage Class
class Message(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    
    @commands.Cog.listener('on_message')
    async def  onMessage(self, message:nextcord.Message):
        """Triggered when a user leaves the server"""
        Object = message
        if message.channel.id == Options['Channels']['Announcement']:
            if "--embed" in message.content:
                Embed = await Custom(
                    f"New Announcement!",
                    f"{message.content}\n\n{message.author.name}#{message.author.discriminator}"
                )
                Object = await message.channel.send(
                    content = f"<@&886540581004795904>",
                    embed = Embed
                )
                await message.delete()
            if "--pin" in message.content:
                await Object.pin()


# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Message(bot))