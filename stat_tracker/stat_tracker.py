import discord
from discord.ext import commands
from datetime import datetime, timedelta
import time


class StatTracker(commands.Cog):
    """Tracks the number of posts people make."""

    def __init__(self, bot):
        self.bot = bot
        self.messageDict = {}
        self.resetDay = str(datetime.now().date() + timedelta(days=7))

    @commands.command()
    async def top_overall(self, ctx, *args):
        """Displays user with the most number of messages."""
        message = "The userid with the most messages is: " + \
                  str(max([len(messages),username] for username, messages in self.messageDict.items())[1])
        await ctx.send(message)

    def clear_historical_messages(self):
        """Clears the message dict."""
        print("clearing message dictionary... This is what it had:")
        print(self.messageDict)

        self.messageDict = {}
        print("done.. Now it is this")
        print(self.messageDict)

    @commands.command()
    async def top_channel(self, ctx, *args):
        """Gets top poster of the channel you are in."""
        channel = ctx.message.channel.name
        myDict = {}
        for person in self.messageDict:
            myDict[person] = 0

            for message in self.messageDict[person]:
                if message["channel"] == channel:
                    myDict[person] += 1
        sortedDict = sorted(myDict, key=myDict.get, reverse=True)
        print("top posts for", channel, "\n", sortedDict)

        message = "First Place: %s with %s messages" % (sortedDict[0], myDict[sortedDict[0]])
        await ctx.send(message)

    @commands.command()
    async def my_stats(self, ctx, *args):
        """Gets the users stats and returns the top channels they post in and how many posts they have."""
        tempDict = {}
        for message in self.messageDict[ctx.message.author.name]:
            if message["channel"] in tempDict:
                tempDict[message["channel"]] += 1
            else:
                tempDict[message["channel"]] = 1
        await ctx.message.author.send(tempDict)


    # @commands.command()
    # async def debug(self, ctx, *args):
    #     print(self.messageDict)
    #     print(self.resetDay)











