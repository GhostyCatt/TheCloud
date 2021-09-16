# Library Imports
import nextcord, json, datetime
from nextcord import message
from nextcord.ext import commands

# Options from Json
with open('Config/Options.json') as RawOptions:
    Options = json.load(RawOptions)

# Embed Functions
async def Success(text:str = "Done!", ctx:commands.Context = None) -> nextcord.Embed:
    """
    Success Embed
    -------------

    Returns an embed or a message object.

    * `Text` - Set as description of an embed.
    * `Ctx` - If passed, embed is sent in current channel.
    """
    embed = nextcord.Embed(
        description = f"{text}",
        color = nextcord.Colour.green()
    )
    
    if not ctx:
        return embed
    else:
        message = await ctx.send(embed = embed)    
        return message
    

async def Fail(text:str = "Something went wrong!", ctx:commands.Context = None) -> nextcord.Embed:
    """
    Fail Embed
    ----------

    Returns an embed or a message object.

    * `Text` - Set as description of an embed.
    * `Ctx` - If passed, embed is sent in current channel.
    """
    embed = nextcord.Embed(
        description = f"{text}",
        color = nextcord.Colour.red()
    )
    
    if not ctx:
        return embed
    else:
        message = await ctx.send(embed = embed)    
        return message
    

async def Log(text:str, ctx:commands.Context) -> nextcord.Message:
    """
    Log Embed
    ----------

    Returns a message object.

    * `Text` - Set as description of an embed.
    * `Ctx` - Used to get log channel
    """
    embed = nextcord.Embed(
        description = f"{text}",
        color = nextcord.Colour.blurple(),
        timestamp = datetime.datetime.utcnow()
    )
    
    channel = ctx.guild.get_channel(Options['Channels']['Log'])

    message = await channel.send(embed = embed)
    await message.add_reaction("❄️")
    return message


async def Custom(title:str, description:str) -> nextcord.Embed:
    """
    Custom Embed
    ------------

    Returns an embed object.

    * `Title` - Sets the title of the embed
    * `Description` - Sets the content of the embed.
    """
    embed = nextcord.Embed(
        title = title,
        description = f"{description}",
        color = nextcord.Colour.blurple()
    )
    return embed