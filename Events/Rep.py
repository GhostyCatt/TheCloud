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

        # Get Database connection
        Conn = GetConn()
        with Conn.cursor() as Cur:
            Cur.execute(f'SELECT "Reputation" from "Data" WHERE "ID" = {message.author.id}')
            Reputation = Cur.fetchone()

        # If user doesnt have a table, get variables for one
        if not Reputation:
            if payload.emoji.id == Options['Emojis']['ID']['Upvote']:
                Script = ('INSERT INTO "Data"("ID", "Reputation") VALUES(%s, %s)')
                Values = (message.author.id, 1)
            elif payload.emoji.id == Options['Emojis']['ID']['Downvote']:
                Script = ('INSERT INTO "Data"("ID", "Reputation") VALUES(%s, %s)')
                Values = (message.author.id, -1)
        
        # Get scripts to update a table
        else:
            if payload.emoji.id == Options['Emojis']['ID']['Upvote']:
                Script = ('UPDATE "Data" SET "Reputation" = %s WHERE "ID" = %s')
                Values = (Reputation[0] + 1, message.author.id)
            elif payload.emoji.id == Options['Emojis']['ID']['Downvote']:
                Script = ('UPDATE "Data" SET "Reputation" = %s WHERE "ID" = %s')
                Values = (Reputation[0] - 1, message.author.id)

        with Conn.cursor() as Cur:
            Cur.execute(Script, Values)
            Conn.commit()
            Conn.close()
            

# Setup the bot
def setup(bot:commands.Bot):
    bot.add_cog(RepHandler(bot))