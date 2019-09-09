from discord.ext import commands
from managers import GameManager
import json
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
                #print("Channel already exists")
                makeChannel = False
                break
        if makeChannel is True:
            await guild.create_voice_channel(lobbyName)
            await guild.create_text_channel(lobbyName)

        makeRole = True
        for role in guild.roles:
            #print(role)
            if "muted" in str(role):
                #print("Role already exists")
                makeRole = False
                break
        if makeRole is True:
            await guild.create_role(name="muted")


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

    log.info(f'[{message.channel.id} | {message.channel}] {message.author} - {message.content}')

    await bot.process_commands(message)

@bot.event 
async def on_voice_state_update(member, begin, end):
    if end.channel.name == "lobby":
        if(member.nick is not None):
            log.info(str(member.nick)+" has joined the lobby")
        else:
            log.info(str(member)+" has joined the lobby")

        introMessage = "Welcome to the lobby! If you need help with the game type \n ```!helpRoles ```"

        await member.send(introMessage)

@commands.command()
async def helpRoles(ctx):
    """Moves everyone to channel."""
    message = "Roles:\n"
    with open('./models/roles.json', 'r') as roleJson:
        roles = json.load(roleJson)
        for role in roles:
            print(roles[role])
            message += "```Name:" + roles[role]["name"] + "\n"
            message += "alignment:" + str(roles[role]["alignment"]) + "\n"
            message += "summary:" + str(roles[role]["summary"]) + "\n"
            message += "abilities:" + str(roles[role]["abilities"]) + "\n"
            message += "attributes:" + str(roles[role]["attributes"]) + "\n"
            message += "goal:" + str(roles[role]["goal"]) + "```\n"
    await ctx.message.author.send(message)

def setup():
    gameManager = GameManager(bot)
    bot.add_cog(gameManager)
    bot.add_command(helpRoles)

if __name__ == "__main__":
    # Initialize Logging
    log = logger.setup_custom_logging("tod")
    log.debug("Logging Setup")

    # Configure Bot Cogs
    setup()

    # Run Bot
    with open('secretkey.txt') as f:
        token = str(f.read())
    bot.run(token)
    log.info("Bot Started...")



















