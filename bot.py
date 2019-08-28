import discord
from discord.ext import commands
from game_manager import game_manager
from charager_manager import character_manager
from datetime import datetime
import csv


description = '''A town of salem knock off.'''


bot = commands.Bot(command_prefix='!', description=description)
gameManager = game_manager.GameManager(bot)
charaterManager = character_manager.CharaterManager(bot)
bot.add_cog(gameManager)
bot.add_cog(charaterManager)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    lobbyName = "lobby"
    for guild in bot.guilds:
        makeChannel = True
        for channel in guild.channels:
            if lobbyName in str(channel):
                print("Channel already exists")
                makeChannel = False
                break
        if makeChannel is True:
            await guild.create_voice_channel(lobbyName)
            await guild.create_text_channel(lobbyName)


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    global last_time

    if message.content.lower() == "f":
        if message.author.nick:
            await message.channel.send(message.author.nick + " has paid respect.")
        else:
            await message.channel.send(message.author.name + " has paid respect.")
    await bot.process_commands(message)

@bot.event 
async def on_voice_state_update(member, begin, end):
    if end.channel.name == "lobby":
        if(member.nick is not None):
            print(str(member.nick)+" has joined the lobby");
        else:
            print(str(member)+" has joined the lobby")

bot.run(token)
