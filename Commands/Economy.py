# Library Imports
import nextcord, json, mysql.connector, os, random, math
from nextcord.ext import commands
from dotenv import load_dotenv
load_dotenv()

# Custom Imports
from Functions.Embed import *
from Views.Work import WorkView

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)
with open('Config/Economy.json') as RawEco:
    Eco = json.load(RawEco)
with open('Config/Work.json') as RawWork:
    Work = json.load(RawWork)

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
            
            # Close connections
            Cur.close()
            db.close()
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
    async def  profile(self, ctx:commands.Context, user: nextcord.Member = None):
        """Check our your profile"""
        await ctx.channel.trigger_typing()

        # Set user to author
        if not user:
            user = ctx.author

        # Connect to database
        db = mysql.connector.connect(
            host = str(os.getenv("Host")),
            user = "ghostyy",
            passwd = str(os.getenv("Password"))
        )
        Cur = db.cursor()

        # Fetch the users profile
        Cur.execute(f"SELECT * FROM `thecloud`.`economy` WHERE UserID = {user.id}")
        Profile = Cur.fetchone()

        if not Profile:
            await Fail(f"You don't have a profile! Make one with `{Options['Prefix']}reg`", ctx)

            # Close connections
            Cur.close()
            db.close()
            return

        # Close connections
        Cur.close()
        db.close()

        # Build up the embed
        embed = await Custom(
            f"{user}'s Profile",
            f"This is {user.name}'s profile on TheCloud!"
        )
        embed.add_field(name = "Balance", value = f"{Options['Emojis']['Coin']} {Profile[1]} / {Profile[2]}", inline = False)
        embed.add_field(name = "Powerup", value = f"{Profile[4]}", inline = False)
        embed.add_field(name = "Boxes", value = f"{Options['Emojis']['Lemon']} {Profile[5]}\n{Options['Emojis']['Blueberry']} {Profile[6]}\n{Options['Emojis']['Grape']} {Profile[7]}", inline = False)
        if not Profile[9]: embed.add_field(name = "Pet", value = "No pet found :(", inline = False)
        else: 
            PetProfile = Eco['Pets'][Profile[9]]
            embed.add_field(name = "Pet", value = f"{PetProfile['Icon']} {PetProfile['Name']} ( **{Profile[10]}** )", inline = False)
        if user.avatar.url: embed.set_thumbnail(url = user.avatar.url)

        # Send the embed
        await ctx.send(embed = embed)

    @commands.command(name = "Work", aliases = ["Job"])
    @commands.cooldown(1, 500, commands.BucketType.member)
    async def  work(self, ctx:commands.Context):
        """Earn some MONEYYY"""
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
            
            # Close connections
            Cur.close()
            db.close()
            return

        # Decide the challenge
        Question = random.choice(random.choice(Work['Work'])['Questions'])
        
        # Build the question embed
        Shuffled = Question['Options'].copy()
        random.shuffle(Shuffled)
        OptionsStr = ''
        Count = 1
        for Option in Shuffled:
            OptionsStr += f"**[`{Count}`]** {Option}\n"
            Count += 1

        # Send the embed
        embed = await Custom(title = f"{Question['Question']}", description = OptionsStr)
        view = WorkView(ctx)

        await ctx.send(embed = embed, view = view)
        
        # Decide reward
        RewardBase = random.randint(100, 4000)
        Reward = RewardBase
        if Profile[9]: # Add pet bonus
            Reward += Eco['Pets'][Profile[9]]['Abilities']['Bonus']
        if Profile[4]: # Add powerup bonus
            Reward += Profile[4]

        # Wait for the user to select an option, of correct, dep coins :]
        try:
            await view.wait()

            if view.value == 0:
                if Question['Options'][0] == Shuffled[0]:
                    await Success(f"That's correct! `{RewardBase}` coins were added to your account!\nBonus Coins: {Reward - RewardBase}", ctx)
                    Cur.execute("UPDATE `thecloud`.`economy` SET Pocket = %s WHERE UserID = %s", (Profile[1] + Reward, ctx.author.id))
                    db.commit()
                else: await Fail(f"That's not the answer...", ctx)
            elif view.value == 1:
                if Question['Options'][0] == Shuffled[1]:
                    await Success(f"That's correct! `{RewardBase}` coins were added to your account!\nBonus Coins: {Reward - RewardBase}", ctx)
                    Cur.execute("UPDATE `thecloud`.`economy` SET Pocket = %s WHERE UserID = %s", (Profile[1] + Reward, ctx.author.id))
                    db.commit()
                else: await Fail(f"That's not the answer...", ctx)
            elif view.value == 2:
                if Question['Options'][0] == Shuffled[2]:
                    await Success(f"That's correct! `{RewardBase}` coins were added to your account!\nBonus Coins: {Reward - RewardBase}", ctx)
                    Cur.execute("UPDATE `thecloud`.`economy` SET Pocket = %s WHERE UserID = %s", (Profile[1] + Reward, ctx.author.id))
                    db.commit()
                else: await Fail(f"That's not the answer...", ctx)
        except:pass
        
        # Close connections
        Cur.close()
        db.close()


    @commands.command(name = "Balance", aliases = ["Bal"])
    async def  bal(self, ctx:commands.Context, user: nextcord.Member = None):
        """Check our your balance"""
        await ctx.channel.trigger_typing()

        # Set user to author
        if not user:
            user = ctx.author

        # Connect to database
        db = mysql.connector.connect(
            host = str(os.getenv("Host")),
            user = "ghostyy",
            passwd = str(os.getenv("Password"))
        )
        Cur = db.cursor()

        # Fetch the users profile
        Cur.execute(f"SELECT * FROM `thecloud`.`economy` WHERE UserID = {user.id}")
        Profile = Cur.fetchone()

        if not Profile:
            await Fail(f"You don't have a profile! Make one with `{Options['Prefix']}reg`", ctx)
            
            # Close connections
            Cur.close()
            db.close()
            return

        # Close connections
        Cur.close()
        db.close()

        # Build up the embed
        embed = await Custom(
            f"{user}'s Profile",
            f"Pocket : {Options['Emojis']['Coin']} {Profile[1]}\nBank : {Options['Emojis']['Coin']} {Profile[2]} / {Profile[3]} "  
        )
        if user.avatar.url: embed.set_thumbnail(url = user.avatar.url)

        # Send the embed
        await ctx.send(embed = embed)


    @commands.command(name = "Deposit", aliases = ["Dep"])
    async def  deposit(self, ctx:commands.Context, amount: int):
        """Deposit money from your pocket to your bank"""
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
            
            # Close connections
            Cur.close()
            db.close()
            return

        # Check if the deposit is possible
        if Profile[1] < amount: 
            await Fail(f"You don't have {amount} in your pocket...", ctx)

            # Close connections
            Cur.close()
            db.close()
            return
        if Profile[2] + amount > Profile[3]:
            await Fail(f"Your bank doens't seem to have that much space...", ctx)

            # Close connections
            Cur.close()
            db.close()
            return

        # Modify the db
        Cur.execute("UPDATE `thecloud`.`economy` SET Pocket = %s, Bank = %s WHERE UserID = %s", (Profile[1] - amount, Profile[2] + amount, ctx.author.id))
        db.commit()
        
        # Send a success embed
        await Success(f"{Options['Emojis']['Coin']} {amount} was deposited to your bank!", ctx)

        # Close connections
        Cur.close()
        db.close()

    
    @commands.command(name = "Deposit", aliases = ["Dep"])
    async def  deposit(self, ctx:commands.Context, amount: int):
        """Deposit money from your pocket to your bank"""
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
            
            # Close connections
            Cur.close()
            db.close()
            return

        # Check if the deposit is possible
        if Profile[2] < amount: 
            await Fail(f"You don't have {amount} in your bank...", ctx)

            # Close connections
            Cur.close()
            db.close()
            return

        # Modify the db
        Cur.execute("UPDATE `thecloud`.`economy` SET Pocket = %s, Bank = %s WHERE UserID = %s", (Profile[1] + amount, Profile[2] - amount, ctx.author.id))
        db.commit()
        
        # Send a success embed
        await Success(f"{Options['Emojis']['Coin']} {amount} was withdrawn to your bank!", ctx)

        # Close connections
        Cur.close()
        db.close()

    
# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(EcoHandler(bot))