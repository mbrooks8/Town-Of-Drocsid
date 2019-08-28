import discord
from discord.ext import commands
from datetime import datetime, timedelta
import time


class GameManager(commands.Cog):
    """Tracks the number of posts people make."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def some_command(self, ctx, *args):
        """Say some shit."""
        message = "go fuck yourself"
        await ctx.message.author.send(message)











