from utils.constants import PREFIX
from discord.ext import commands
import discord
import json

# Help Menu
def command_help(command) -> str:
    """
    Creates a help entry for a command
    :param command: a discord command object
    :returns: an entry with command name, description, arguments
    """
    arguments = ''.join((f' [{argument}]' for argument in command.clean_params))
    return f'`{PREFIX}{command.name}{arguments}`: {command.description}'

class Help(commands.HelpCommand):
    async def send_bot_help(self, *_):
        command_list = sorted([command for command in client.commands if command.name != 'help'], key=lambda x:x.name)
        await self.get_destination().send(
            embed=discord.Embed(
                title='Commands',
                description=f'Prefix: `{PREFIX}` | Total commands: `{len(command_list)}`',
                color=self.get_destination().guild.me.color,
            ).set_author(
                name=client.user.name,
                icon_url=client.user.avatar_url
            ).set_thumbnail(
                url=client.user.avatar_url
            ).add_field(
                name='\u200b',
                value='\n\n'.join(command_help(command) for command in command_list),
                inline=False
            )
        )
    
    async def send_command_help(self, command):
        await self.get_destination().send(command_help(command) + (f'\n\n```{command.help}```' if command.help else ''))

    async def send_error_message(self, *_):
        await self.get_destination().send('Command not found')

# Create Client with Intents
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=Help(),
    status=discord.Status.online,
    activity=discord.Activity(type=discord.ActivityType.watching, name='sus')
)

# Read whitelisted channels and triggers from file
def load_amogus():
    with open('logs/sus.json') as file:
        client.sus = json.load(file)
    with open('logs/whitelist.json') as file:
        client.whitelist = json.load(file)['channels']
load_amogus()

# Custom Exception
class SkillIssue(commands.CommandError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)