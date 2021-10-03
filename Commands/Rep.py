# Library Imports
import nextcord, json, mysql.connector, os
from nextcord.ext import commands
from dotenv import load_dotenv
load_dotenv()

# Custom Imports
from Functions.Embed import *

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
        
        # Connect to database
        db = mysql.connector.connect(
            host = str(os.getenv("Host")),
            user = "ghostyy",
            passwd = str(os.getenv("Password"))
        )

        # Get cursor and attempt to get reputation
        Cur = db.cursor()
        Cur.execute("SELECT * FROM `thecloud`.`reputation` WHERE UserID = {}".format(user.id))
        Profile = Cur.fetchone()

        # Check if the profile exists, if not, send an embed
        if not Profile:
            await Fail(f"You don't have any rep yet!\n\nNote: Rep is handled using {Options['Emojis']['Upvote']} & {Options['Emojis']['Downvote']} reactions.", ctx)
            return
        
        # Construct the profile embed
        embed = await Custom(
            f"{user}",
            f"Your reputation on this server is: **{Profile[1]}\n**!\nUpvotes: **{Profile[2]}**\nDownvotes : **{Profile[3]}**"
        )   
        embed.set_thumbnail(url = user.avatar.url)

        # Send the profile embed
        await ctx.send(embed = embed)

        # Close and commit everything
        Cur.close()
        db.commit()
        db.close()


    @commands.command(name = "Leaderboard", aliases = ["Lb"])
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def  leaderboard(self, ctx: commands.Context, users:int = 10):
        """The rep leaderboard"""
        await ctx.channel.trigger_typing()
        
        # Limit users to 100
        if users > 100:
            users = 100
        
        # Connect to database
        db = mysql.connector.connect(
            host = str(os.getenv("Host")),
            user = "ghostyy",
            passwd = str(os.getenv("Password"))
        )

        # Get cursor and attempt to get reputation
        Cur = db.cursor(buffered = True)
        Cur.execute("SELECT * FROM `thecloud`.`reputation` ORDER BY `Reputation` DESC")
        Profiles = Cur.fetchmany(users)

        # Build the embed
        repstring, count = '', 1
        for Profile in Profiles:
            User = ctx.guild.get_member(Profile[0])
            if not User: pass
            else:
                if count == 1: repstring += f'🥇 **{count}.**  {User.name} : {Profile[1]}\n'
                elif count == 2: repstring += f'🥈 **{count}.**  {User.name} : {Profile[1]}\n'
                elif count == 3: repstring += f'🥉 **{count}.**  {User.name} : {Profile[1]}\n'
                else: repstring += f'**{count}.**  {User.name} : {Profile[1]}\n'
                count += 1
        
        embed = await Custom(title = f'Top {users} Leaderboard', description = repstring)

        # Send the profile embed
        await ctx.send(embed = embed)

        # Close and commit everything
        Cur.close()
        db.commit()
        db.close()

# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(Rep(bot))