import discord
import datetime
from discord.ext import commands
import random
from stat_tracker import stat_tracker
from datetime import datetime

import csv


# Test token: NTYzMDUxMTA2ODkzMDM3NTk4.XKTzBA.kCuGuv8Onok8NZZm1Q5TfPfrGAc
token = 'NTYzMDUxMTA2ODkzMDM3NTk4.XKTzBA.kCuGuv8Onok8NZZm1Q5TfPfrGAc'

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

bot = commands.Bot(command_prefix='&', description=description)
bot.add_cog(fanfic_seeker.FanficSeeker(bot))
bot.add_cog(prompt_generator.PromptGenerator(bot))
stat = stat_tracker.StatTracker(bot)
bot.add_cog(stat)
# bot.add_cog(Cleanup(bot))
# USEABLE_CATS = ["💕 Sora & Kairi", "🔑 Kingdom Hearts"]
users_counts = {}
# MIN_TUMBLR_DELAY_MINUTES = 60
last_time = datetime.utcnow()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


"""
Press F to pay respects
"""
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    global last_time
    # if message.created_at - last_time > datetime.timedelta(minutes=MIN_TUMBLR_DELAY_MINUTES):
    #     links = secret_parser.get_new_links(last_time)
    #     for result in links:
    #         await _send_link_to_channel(message, result)
    #     last_time = message.created_at

    if str(datetime.now().date()) == stat.resetDay:
        print("It is reset day")

        filename = "messageHistory" + str(datetime.now().date()) + ".txt"
        print("Creating file:", filename)
        f = open(filename, "w")
        print("Saving message history into this file")
        f.write(stat.messageDict)
        f.close

        stat.clear_historical_messages()
        stat.resetDay = str(datetime.now().date() + timedelta(days=7))


    if message.author.name in stat.messageDict:
        stat.messageDict[message.author.name] += [{'message': message.content,
                                                 'channel': message.channel.name,
                                                 'date': str(datetime.now().date()),
                                                 'time': str(datetime.now().time())}]
        #print(stat.messageDict)
    else:
        stat.messageDict[message.author.name] = [{'message': message.content,
                                                'channel': message.channel.name,
                                                'date': str(datetime.now().date()),
                                                'time': str(datetime.now().time())}]
        #print(stat.messageDict)

    #if datetime.now().time()
    if message.content.lower() == "f":
        if message.author.nick:
            await message.channel.send(message.author.nick + " has paid respect.")
        else:
            await message.channel.send(message.author.name + " has paid respect.")
    await bot.process_commands(message)


bot.run(token)
