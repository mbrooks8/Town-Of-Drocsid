import discord
from discord.ext import commands
from datetime import datetime, timedelta
import time


class GameManager(commands.Cog):
    """Manages the game."""

    def __init__(self, bot):
        self.bot = bot
        self.started = False
        self.players = []

    @commands.command()
    async def leave(self, ctx, *args):
        """Lets Players Leave The Game."""
        if ctx.message.author.name in self.players:
            message = ctx.message.author.name + "has left the game"
            self.players.pop(ctx.message.author.name, None)
            await ctx.send(message)
        else:
            await ctx.send("You are not part of this game.")

    @commands.command()
    async def players(self, ctx, *args):
        """Lists the players."""
        message = "```These are the players:\n"
        for player in self.players:
            message += player.name + "\n"
        message += "```"
        await ctx.send(message)

    @commands.command()
    async def start(self, ctx, *args):
        """Starts the game."""
        gameChannel = "Town Of Discord"
        channel = ctx.message.author.voice.channel
        print("The channel is:", str(channel))

        if "lobby" in str(channel):
            lobby = channel
            if len(lobby.members) < 1:
                message = "There are not enough players in the game. Please make more friends"
                await ctx.send(message)

            else:
                self.started = True

                makeChannel = True
                for channel in ctx.guild.channels:
                    if gameChannel in str(channel):
                        makeChannel = False
                        break

                if makeChannel is True:
                    await ctx.message.guild.create_voice_channel(gameChannel)
                    await ctx.message.guild.create_text_channel(gameChannel)

                for channel in ctx.message.guild.channels:
                    if channel.name == gameChannel:
                        theGameChannel = channel

                for member in lobby.members:
                    self.players.append(member)
                    await member.move_to(theGameChannel)

                message = "The Game Has Started"
                await ctx.send(message)

        else:
            message = "You must be in the lobby to start the game"
            await ctx.send(message)


    @commands.command()
    async def end(self, ctx, *args):
        """Forces the game to end."""
        self.started = False
        for channel in ctx.guild.channels:
            if "discord" in str(channel).lower():
                print(channel)
                await channel.delete()
        message = "The Game Has Been Forcefully Stopped by" + ctx.message.author.name
        await ctx.send(message)


    @commands.command()
    async def moveAll(self, ctx, *args):
        """Moves everyone to channel."""
        for channel in ctx.guild.channels:
            if "lobby" in str(channel):
                lobby = channel
                break
        print(ctx.guild.members)
        for member in ctx.guild.members:
            print("Moving user to lobby")
            await member.move_to(lobby)

    @commands.command()
    async def messageAll(self, ctx, *args):
        """Moves everyone to channel."""
        for channel in ctx.guild.channels:
            if "lobby" in str(channel):
                lobby = channel
                break

        for member in lobby.members:
            await member.send("hello")







