import discord
from discord.ext import commands
from gameFiles import gameManager
from datetime import datetime
import csv

token = 'NjE2MTA1OTY1NjAyOTk2MjQ0.XWXzRA.upQMPy5A0k_QZa1mkbmAbK8pUdI'

description = '''A town of salem knock off.'''

bot = commands.Bot(command_prefix='!', description=description)
gameManager = gameManager.GameManager(bot)
bot.add_cog(gameManager)

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
