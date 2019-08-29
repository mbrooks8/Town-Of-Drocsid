import discord
from managers import character_manager 
from discord.ext import commands
from datetime import datetime, timedelta
import time


class GameManager(commands.Cog):
    """Manages the game."""
    #Phases of the game are:
    #night -- 0
    #discussion & voting -- 1
    #Judgement -- 2
    def __init__(self, bot):
        self.bot = bot
        self.started = False
        self.players = []
        self.characterManager = character_manager.CharaterManager()
        self.phase = 1

    @commands.command()
    async def move(self, ctx, *args):
        """Moves the phase of the game to the next phase."""
        #Night: Lock chat channel and mute voice channel
        #Discussion: open voice channel unlock chat channel
        #Judgement: mute all players except the voted player and block everyone from posting in chat channel except the voted player
        self.phase = (self.phase + 1)%3
        print("this is the phase", self.phase)

        for guild in ctx.bot.guilds:
            for role in guild.roles:
                #print(role)
                if "muted" in str(role):
                    muted = role
            if self.phase == 0:
                for member in self.players:
                    print(member)
                    await member.add_roles(muted)
            if self.phase == 1:
                for member in self.players:
                    print(member)
                    await member.remove_roles(muted)
            if self.phase == 2:
                for member in self.players:
                    print(member)
                    await member.add_roles(muted)


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
            username = player.nick
            if username is None:
                username = player.name
            message += username + "\n"
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

                self.characterManager.initCharacters(self.players)

                for player in self.characterManager.players:
                    message = "Hello" + player.member.name + " Welcome to Town of Discord! The game has started. You have the role of:\n"
                    print("blah blah",player.role)
                    message += player.role["name"] + "\n"
                    message += str(player.role["alignment"]) + "\n"
                    message += str(player.alive) + "\n"

                message += "The Game Has Started"
                
                await ctx.send(message)

        else:
            message = "You must be in the lobby to start the game"
            await ctx.send(message)


    @commands.command()
    async def end(self, ctx, *args):
        """Forces the game to end."""
        self.started = False

        #moves all users to the lobby
        for channel in ctx.guild.channels:
            if "lobby" in str(channel):
                lobby = channel
                break
        for member in ctx.guild.members:
            if member.voice is not None:
                print("Moving user to lobby")
                await member.move_to(lobby)

        #deletes game channels
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







