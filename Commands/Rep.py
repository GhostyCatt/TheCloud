# Library Imports
import nextcord, json
from nextcord.ext import commands

# Custom Imports
from Functions.Embed import *
from Functions.Database import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

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
        
        # Get Database connection
        Conn = GetConn()
        with Conn.cursor() as Cur:
            Cur.execute(f'SELECT "Reputation" from "Data" WHERE "ID" = {user.id}')
            Reputation = Cur.fetchone()
        

        # Check if the profile exists, if not, send an embed
        if not Reputation:
            await Fail(f"You don't have any rep yet!", ctx)
            return
        
        # Construct the profile embed
        embed = await Custom(
            f"{user}",
            f"Your reputation on this server is: **{Reputation[0]}**!\n\nNote: Rep is handled using {Options['Emojis']['Upvote']} & {Options['Emojis']['Downvote']} reactions."
        )
        embed.set_thumbnail(url = user.avatar.url)

        # Send the profile embed
        await ctx.send(embed = embed)


# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Rep(bot))