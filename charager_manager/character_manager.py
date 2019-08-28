import discord
from discord.ext import commands
from datetime import datetime, timedelta
import time


class CharaterManager(commands.Cog):
    """Tracks the number of posts people make."""
    bot = commands.Bot(command_prefix='!')
    print("character class made")
    class character():
        def __init__(self, name, role):
            self.name = name
            self.role = role
            self.alive = alive
        
        def setName(self, name):
            self.name = name
        
        def setRole(self, role):
            self.role = role
        
        def setAlive(self, alive):
            self.alive = alive

    def __init__(self, bot):
        self.bot = bot

        
    @bot.event
    async def on_voice_state_update(member, begin, end):
        if end.channel.name == "lobby":
            if(member.nick is not None):
                print(str(member.nick)+" has joined the lobby");
            else:
                print(str(member)+" has joined the lobby")
    
'''
import discord

TOKEN = 'NjE2MTIyMTQ3NDI4ODkyNzAz.XWX--g.4Rqtb6qdOjNFBcODSkNFjvJ9ZUw'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

@client.event
async def on_voice_state_update(member, begin, end):
    if end.channel.name == "lobby":
        if(member.nick is not None):
            print(str(member.nick)+" has joined the lobby");
        else:
            print(str(member)+" has joined the lobby")

client.run(TOKEN)

'''

