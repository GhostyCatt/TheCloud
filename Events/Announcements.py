# Library Imports
import nextcord, json
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# onMessage Class
class Tags(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    
    @commands.Cog.listener('on_message')
    async def  TagsDetection(self, message:nextcord.Message):
        """Triggered when a user leaves the server"""
        # Bot check
        if message.author.bot: return

        # Set a variable for the message
        Object = message

        # Check if the message is in the announcements channel
        if message.channel.id == Options['Channels']['Announcement']:
            # Create the object and send it
            Embed = await Custom(
                f"New Announcement!",
                f"{message.content}\n\nAnnouncement by : {message.author.name}#{message.author.discriminator}"
            )
            Object = await message.channel.send(embed = Embed)

            # Delete the old message
            await message.delete()

            # If the message had the pin tag, pin it
            if "--pin" in message.content:
                await Object.pin()


# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Tags(bot))