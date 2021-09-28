# Library Imports
import nextcord, json, mysql.connector, os
from nextcord.ext import commands
from dotenv import load_dotenv
load_dotenv()

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Reputation Class
class RepHandler(commands.Cog):
    """The class that handles all rep related features"""
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener('on_raw_reaction_add')
    async def  RepDetection(self, payload:nextcord.RawReactionActionEvent):
        """Triggered when a reaction is added"""
        # Return if the reaction isn't a upvote or downvote
        if not payload.emoji.id in [ Options['Emojis']['ID']['Upvote'], Options['Emojis']['ID']['Downvote'] ]:
            return
        
        # Get the message object
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

        # Return if its a self upvote / downvote
        if message.author.id == payload.user_id:
            return
        
        # Return if its a bot
        if message.author.bot:
            return
        
        # Connect to database
        db = mysql.connector.connect(
            host = str(os.getenv("Host")),
            user = "ghostyy",
            passwd = str(os.getenv("Password"))
        )
        
        # Get cursor and attempt to get reputation
        Cur = db.cursor()
        Cur.execute("SELECT Reputation FROM `thecloud`.`reputation` WHERE UserID = {}".format(message.author.id))
        Reputation = Cur.fetchone()

        # If no reputation was found, get args to insert a new row
        if not Reputation:
            if payload.emoji.id == Options['Emojis']['ID']['Upvote']:
                Script = ('INSERT INTO `thecloud`.`reputation`(UserID, Reputation, Upvotes) VALUES(%s, %s, %s)')
                Values = (message.author.id, 1, 1)
            elif payload.emoji.id == Options['Emojis']['ID']['Downvote']:
                Script = ('INSERT INTO `thecloud`.`reputation`(UserID, Reputation, Downvotes) VALUES(%s, %s, %s)')
                Values = (message.author.id, 1, -1)
        
        # If rep was found, update it
        else:
            if payload.emoji.id == Options['Emojis']['ID']['Upvote']:
                Script = ('UPDATE `thecloud`.`reputation` SET Reputation = %s WHERE UserID = %s')
                Values = (Reputation[0] + 1, message.author.id)
            elif payload.emoji.id == Options['Emojis']['ID']['Downvote']:
                Script = ('UPDATE `thecloud`.`reputation` SET Reputation = %s WHERE UserID = %s')
                Values = (Reputation[0] - 1, message.author.id)
        
        # Execute the args
        Cur.execute(Script, Values)

        # Close and commit everything
        Cur.close()
        db.commit()
        db.close()

    
# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(RepHandler(bot))