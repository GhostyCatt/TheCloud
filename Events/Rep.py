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
class RepHandler(commands.Cog):
    def __init__(self, bot:commands.Bot):
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

        # Get the users profile from the database
        UserProfile = Collection.find_one({ "_id": int(message.author.id) })

        # If the profile doesn't exist, add it!
        if not UserProfile:
            with open('Config/Schema/UserData.json', 'r') as RawUserData:
                UserData = json.load(RawUserData)
            
            UserData['_id'] = int(message.author.id)

            Collection.insert_one(UserData)
            UserProfile = UserData
        
        # Check if the reaction is an upvote or downvote
        if payload.emoji.id == Options['Emojis']['ID']['Upvote']:
            CurrentVotes = UserProfile['Rep']['Upvotes']
            TotalRep = UserProfile['Rep']['Total']

            Collection.update_one(
                { "_id" : int(message.author.id) }, 
                { "$set" : { "Rep.Upvotes" : int(CurrentVotes + 1) } }
            )
            Collection.update_one(
                { "_id" : int(message.author.id) }, 
                { "$set" : { "Rep.Total" : int(TotalRep + 1) } }
            )

        
        elif payload.emoji.id == Options['Emojis']['ID']['Downvote']:
            CurrentVotes = UserProfile['Rep']['Downvotes']
            TotalRep = UserProfile['Rep']['Total']

            Collection.update_one(
                { "_id" : int(message.author.id) }, 
                { "$set" : { "Rep.Downvotes" : int(CurrentVotes + 1) } }
            )
            Collection.update_one(
                { "_id" : int(message.author.id) }, 
                { "$set" : { "Rep.Total" : int(TotalRep - 1) } }
            )
        
        else: pass
            

# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(RepHandler(bot))