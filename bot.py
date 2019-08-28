import discord
from discord.ext import commands
from game_manager import game_manager
from charager_manager import character_manager
from datetime import datetime
import csv

token = 'NjE2MTA1OTY1NjAyOTk2MjQ0.XWX5DA.xKKjCPtdVjEqGRewlAG5oJ0LK9o'

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


bot.run(token)
