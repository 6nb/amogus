import discord
import json

def operator(ctx) -> bool:
    """
    Check function to see if message was sent by a bot operator
    :param ctx: command context
    :returns: whether or not the author is a bot operator
    """
    with open('logs/whitelist.json') as file:
        return ctx.author.id in json.load(file)['operators']

def interpret(ctx, query:str) -> discord.channel:
    """
    Interpret channel parameter
    :param ctx: command context
    :param query: channel name or id
    :returns: discord channel object
    """
    if ctx.message.channel_mentions: return ctx.message.channel_mentions[0]
    try:
        search = ctx.guild.get_channel(int(query)) 
        if not search: raise ValueError
        return search
    except ValueError:
        for obj in ctx.guild.channels:
            if query.lower() == obj.name.lower(): return obj
        for obj in ctx.guild.channels:
            if query.lower() in obj.name.lower(): return obj
        return None