# Library Imports
import nextcord, json, mysql.connector, os, random, math
from nextcord.ext import commands
from dotenv import load_dotenv
load_dotenv()

# Custom Imports
from Functions.Embed import *

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)
with open('Config/Economy.json') as RawEco:
    Eco = json.load(RawEco)

# Reputation Class
class EcoHandler(commands.Cog):
    """The class that handles all economy related features"""
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name = "Register", aliases = ["Reg"])
    async def  register(self, ctx:commands.Context):
        """Register yourself to our economy system"""
        await ctx.channel.trigger_typing()

        # Connect to database
        db = mysql.connector.connect(
            host = str(os.getenv("Host")),
            user = "ghostyy",
            passwd = str(os.getenv("Password"))
        )
        Cur = db.cursor()

        # Check if user already has a profile
        Cur.execute(f"SELECT * FROM `thecloud`.`economy` WHERE UserID = {ctx.author.id}")
        Profile = Cur.fetchone()

        if Profile:
            await Fail("You already have a profile!", ctx)
            return
        
        # Build up profile [ 5% chance for lemon box ]
        def roundup(x): return int(math.ceil(x / 100.0)) * 100

        Coins = random.randint(100, 10000)
        LemChance = random.randint(1, 100)
        if  LemChance < 5:
            Script = ('INSERT INTO `thecloud`.`economy`(UserID, Pocket, BankMax, Box_Lemon) VALUES(%s, %s, %s, %s)')
            Values = (ctx.author.id, roundup(Coins), 100000, 1)
        else:
            Script = ('INSERT INTO `thecloud`.`economy`(UserID, Pocket, BankMax) VALUES(%s, %s, %s)')
            Values = (ctx.author.id, roundup(Coins), 100000)
        
        # Commit changes
        Cur.execute(Script, Values)
        db.commit()

        # Send a success embed(s)
        await Success(f"Your profile was created with **{roundup(Coins)}** bonus coins!", ctx)
        if LemChance < 5: await Success(f"You just got a Lemon Crate!", ctx)
        else: pass
        
        # Close connections
        Cur.close()
        db.close()
    

    @commands.command(name = "Profile", aliases = ["Prof"])
    async def  profile(self, ctx:commands.Context):
        """Check our your profile"""
        await ctx.channel.trigger_typing()

        # Connect to database
        db = mysql.connector.connect(
            host = str(os.getenv("Host")),
            user = "ghostyy",
            passwd = str(os.getenv("Password"))
        )
        Cur = db.cursor()

        # Fetch the users profile
        Cur.execute(f"SELECT * FROM `thecloud`.`economy` WHERE UserID = {ctx.author.id}")
        Profile = Cur.fetchone()

        if not Profile:
            await Fail(f"You don't have a profile! Make one with `{Options['Prefix']}reg`", ctx)
            return

        # Close connections
        Cur.close()
        db.close()

        # Build up the embed
        embed = await Custom(
            f"{ctx.author}'s Profile",
            f"This is {ctx.author.name}'s profile on TheCloud!"
        )
        embed.add_field(name = "Balance", value = f"{Options['Emojis']['Coin']} {Profile[1]} / {Profile[2]}", inline = False)
        embed.add_field(name = "Powerup", value = f"{Profile[4]}", inline = False)
        embed.add_field(name = "Boxes", value = f"{Options['Emojis']['Lemon']} {Profile[5]}\n{Options['Emojis']['Blueberry']} {Profile[6]}\n{Options['Emojis']['Grape']} {Profile[7]}", inline = False)
        if not Profile[9]: embed.add_field(name = "Pet", value = "No pet found :(", inline = False)
        else: 
            PetProfile = Eco['Pets'][Profile[9]]
            embed.add_field(name = "Pet", value = f"{PetProfile['Icon']} {PetProfile['Name']} ( **{Profile[10]}** )", inline = False)
        if ctx.author.avatar.url: embed.set_thumbnail(url = ctx.author.avatar.url)

        # Send the embed
        await ctx.send(embed = embed)

    
# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(EcoHandler(bot))