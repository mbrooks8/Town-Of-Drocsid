from discord.ext import commands
from managers import GameManager
from managers import CharaterManager

from utils import logger

# Initialize Bot
description = '''A town of salem knock off.'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    log.info('Logged in as')
    log.info(bot.user.name)
    log.info(bot.user.id)
    log.info('------')
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
            log.info(str(member.nick)+" has joined the lobby");
        else:
            log.info(str(member)+" has joined the lobby")


def setup():
    gameManager = GameManager(bot)
    charaterManager = CharaterManager(bot)
    bot.add_cog(gameManager)
    bot.add_cog(charaterManager)


if __name__ == "__main__":
    # Initialize Logging
    log = logger.setup_custom_logging("tod")
    log.debug("Logging Setup")

    # Run Bot
    with open('secretkey.txt') as f:
        token = str(f.read())
    bot.run(token)
    log.info("Bot Started...")

    # Configure Bot Cogs
    setup()
