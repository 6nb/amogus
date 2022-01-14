from utils.client import client, SkillIssue, load_amogus
from utils.constants import PREFIX, TOKEN, SAVE_CHANNEL
from utils.methods import operator, interpret
from discord.ext import commands
import discord
import random
import json

@client.event
async def on_ready():
    print(f'Online as {client.user}\n')

@client.event
async def on_message(message):

    if message.author.bot or message.author == client.user:
        return

    # Command Handling
    if message.content.startswith(PREFIX):
        await client.process_commands(message)

    elif message.channel.id in client.whitelist:
        trigger, response = next(((key, value) for key, value in client.sus.items() if key in message.content.lower()), (None, None))
        if trigger:
            await message.channel.send(response)
            print(f'Responded to "{trigger}" for {message.author}')
            return

@client.command(description='send a random meme')
async def amogus(ctx):
    await ctx.send(random.choice(list(client.sus.values())))

@client.command(name='channels', aliases=['list'], description='list channels the bot can be triggered in')
@commands.guild_only()
async def list_channels(ctx):

    with open('logs/whitelist.json') as file:
        channels = [f'{channel} ({channel.id})' for channel_id in json.load(file)['channels'] if (channel := ctx.guild.get_channel(channel_id))]

    await ctx.send('```Channels:\n\n' + '\n'.join(channels) + '```' if channels else 'No channels added.')

@client.command(description='add/remove channels to the bot')
@commands.guild_only()
@commands.check(operator)
async def whitelist(ctx, method, *, channel:str=None):
    """
    [method] = "add" or "remove"

    [channel] = a discord channel name or id
    """
    channel = ctx.channel if not channel else interpret(ctx, channel) # custom converting channel param
    if not channel: raise SkillIssue('Channel not found')

    with open('logs/whitelist.json') as file:
        data = json.load(file)

    match(method):
        case 'add' | 'a':
            if channel.id in data['channels']: raise SkillIssue('Channel already whitelisted')
            data['channels'].append(channel.id)
            action = 'Added'
        case 'remove' | 'delete' | 'rm' | 'del' | 'r' | 'd':
            if channel.id not in data['channels']: raise SkillIssue('Channel already not whitelisted')
            data['channels'].remove(channel.id)
            action = 'Removed'
        case _:
            raise commands.BadArgument

    with open('logs/whitelist.json', 'w') as file:
        json.dump(data, file, indent=2)

    await ctx.send(f'{action} channel {channel} ({channel.id})')
    load_amogus()

@client.command(name='add', description='add a meme to the bot')
@commands.check(operator)
async def add_meme(ctx, trigger, *, response:str=None):
    """
    [trigger] = word or phrase to trigger the bot

    [response] = attachment or message the bot will send
    """
    with open('logs/sus.json') as file:
        data = json.load(file)
    
    match (len(ctx.message.attachments)):
        # No attachments: must have response with text/links
        case 0:
            if not response: raise SkillIssue('Must provide image attachment or message')

        # One attachment: save image/video to channel
        case 1:
            file_type = ctx.message.attachments[0].content_type
            image_file = await ctx.message.attachments[0].to_file()
            image_file.filename = f'{trigger}.{file_type[file_type.index("/") + 1:]}'
            try: save = await client.get_channel(SAVE_CHANNEL).send(file=image_file)
            except Exception: raise SkillIssue("Couldn't upload save attachment. If your media is too large, just submit a link instead.")
            response = save.attachments[0].url
        case _: 
            raise SkillIssue('Too many attachments')
    
    # Check duplicates then add
    duplicate = None if trigger not in data else data[trigger]
    data[trigger] = response
    with open('logs/sus.json', 'w') as file:
        json.dump(dict(sorted(data.items(), key=lambda x:len(x[0]), reverse=True)), file, indent=2)
    
    await ctx.send('The funny has been added.')
    if duplicate: await ctx.send(f'Overwrote: `{duplicate}` -> `{data[trigger]}`')
    load_amogus()

@client.command(name='delete', description='remove meme from bot')
@commands.check(operator)
async def delete_meme(ctx, trigger):
    """
    trigger] = word or phrase to delete from the bot
    """
    with open('logs/sus.json') as file:
        data = json.load(file)
    
    if trigger not in data: raise SkillIssue("That trigger word doesn't exist")
    del data[trigger]

    with open('logs/sus.json', 'w') as file:
        json.dump(data, file, indent=2)

    await ctx.send('The funny has been removed. Sad!')
    load_amogus()

@client.command(aliases=['json', 'save'], description='send file of bot trigger words')
@commands.check(operator)
async def logs(ctx):

    with open(f'logs/sus.json', 'rb') as file:
        await ctx.send(file=discord.File(file, 'sus.json'))

# Command Error Handling
@client.event
async def on_command_error(ctx, error):

    if isinstance(error, SkillIssue):
        await ctx.send(error)
    else:
        match(type(error)):
            case commands.CommandNotFound:
                await ctx.send('Command not found.')
                return
            case commands.MissingRequiredArgument:
                await ctx.send(f'Must provide `{error.param.name}` for this command, try `{PREFIX}help {ctx.command}` for usage')
            case commands.BadArgument:
                await ctx.send(f'Wrong arguments, try `{PREFIX}help {ctx.command}` for usage')
            case commands.NoPrivateMessage:
                await ctx.send('Doesnt work in DMs')
            case commands.CheckFailure | commands.MissingPermissions:
                await ctx.send('No perms, SAD!')
            case commands.BotMissingPermissions:
                await ctx.send('I dont have perms to do that :(')
            case _: 
                await ctx.send(f'An error occured executing this command')
                print(f'[EXCEPTION] Type {type(error)} by {ctx.author} with content {ctx.message.content}:\n', error)

try: client.run(TOKEN)
except Exception as error:
    print(f'Failed to log in:', error)