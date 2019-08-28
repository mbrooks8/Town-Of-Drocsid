import discord
from discord.ext import commands
from datetime import datetime, timedelta
import time


class GameManager(commands.Cog):
    """Manages the game."""

    def __init__(self, bot):
        self.bot = bot
        self.started = False
        self.players = {}

    @commands.command()
    async def join(self, ctx, *args):
        """Lets Players Join The Game."""
        if len(self.players) <= 15:
            if ctx.message.author.name not in self.players:
                self.players[ctx.message.author.name] = "something"
                message = ctx.message.author.name, "has joined the game!"
                await ctx.send(message)
            else:
                await ctx.send("You are already part of this game.")
        else:
            await ctx.send("There are already 15 players in this game.")

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
            message += player + "\n```"
        await ctx.send(message)

    @commands.command()
    async def start(self, ctx, *args):
        """Starts the game."""
        if len(self.players) < 1:
            message = "There are not enough players in the game. Please make more friends"
            await ctx.send(message)
        else:
            self.started = True
            await ctx.message.guild.create_voice_channel("Town Of Discord")
            await ctx.message.guild.create_text_channel("Town Of Discord")
            message = "The Game Has Started"
            await ctx.send(message)


    @commands.command()
    async def end(self, ctx, *args):
        """Forces the game to end."""
        self.started = False
        message = "The Game Has Been Forcefully Stopped by" + ctx.message.author.name
        await ctx.send(message)




