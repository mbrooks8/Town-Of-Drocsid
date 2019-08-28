import discord
from discord.ext import commands
from datetime import datetime, timedelta
import time


class CharaterManager(commands.Cog):
    """Tracks the number of posts people make."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def some_command2(self, ctx, *args):
        """Say some shit."""
        message = "holy shit go fuck yourself"
        await ctx.message.author.send(message)











