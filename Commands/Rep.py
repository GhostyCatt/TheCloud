# Library Imports
import nextcord, json, pymongo, os
from nextcord.user import User
from dotenv import load_dotenv
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Get database
load_dotenv()
Client = pymongo.MongoClient(f"mongodb+srv://CloudBot:{os.getenv('MongoPassword')}@cluster0.hwg9f.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
Database = Client['TheCloudDiscord']
Collection = Database['UserData']

# Rep Class
class Rep(commands.Cog):
    """Reputation related commands"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "Rep", aliases = ["Reputation"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  rep(self, ctx: commands.Context, user:nextcord.Member = None):
        """Shows someones rep"""
        await ctx.channel.trigger_typing()

        # Set user to the author if noone was mentioned
        if not user:
            user = ctx.author
        
        # Fetch the profile
        UserProfile = Collection.find_one({ "_id": int(user.id) })

        # Check if the profile exists, if not, send an embed
        if not UserProfile:
            await Fail(f"You don't have any rep yet!", ctx)
            return
        
        # Construct the profile embed
        embed = await Custom(
            f"{user}",
            f"This is the reputation status of {user}"
        )
        embed.add_field(name = "Upvotes", value = UserProfile['Rep']['Upvotes'])
        embed.add_field(name = "Reputation", value = UserProfile['Rep']['Total'])
        embed.add_field(name = "Downvotes", value = UserProfile['Rep']['Downvotes'])
        embed.set_thumbnail(url = user.avatar.url)

        # Send the profile embed
        await ctx.send(embed = embed)


# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Rep(bot))