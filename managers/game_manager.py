import discord
from managers import character_manager 
from discord.ext import commands
from datetime import datetime, timedelta
import time
import asyncio


class GameManager(commands.Cog):
    """Manages the game."""
    # Phases of the game are:
    # night -- 0
    # discussion & voting -- 1
    # Judgement -- 2
    def __init__(self, bot):
        self.bot = bot
        self.started = False
        self.players = []
        self.characterManager = character_manager.CharaterManager()
        self.phase = 0
        self.client = discord.Client()
        self.roles = {}
        self.channels = {}
        self.categories = {}

    async def start_timer(self, delay, what):
        if self.started is True:
            await self.channels["town-of-discord"].send(what)
            await asyncio.sleep(delay)

    async def move(self, ctx):
        """Moves the phase of the game to the next phase."""
        if self.started is True:
            self.phase = (self.phase + 1) % 3
            print("The current phase is:", self.phase)

            if self.phase == 0:
                # Night: Lock chat channel and mute voice channel

                # Mute everyone
                for member in self.players:
                    # print("adding" + str(member) + "to muted discord role")
                    await member.add_roles(self.roles["muted"])

                # let people do their class actions for 30 seconds
                loop = asyncio.get_event_loop()
                task1 = loop.create_task(self.start_timer(10, 'Night Phase Has Started'))
                await task1
                await self.move(self.bot)

            if self.phase == 1:
                # Discussion: open voice channel unlock chat channel
                for member in self.players:
                    # print(member)
                    await member.remove_roles(self.roles["muted"])

                # day lasts for 45 seconds
                loop = asyncio.get_event_loop()
                task1 = loop.create_task(self.start_timer(10, 'Discussion Phase Has Started'))
                await task1
                await self.move(self.bot)

            if self.phase == 2:
                # Judgement: mute all players except the voted player
                # and block everyone from posting in chat channel except the voted player
                for member in self.players:
                    # todo: if the player is not the one that was voted for, mute them.
                    # print(member)
                    await member.add_roles(self.roles["muted"])

                loop = asyncio.get_event_loop()
                task1 = loop.create_task(self.start_timer(10, 'Judgement Phase Has Started'))
                await task1

                end = self.check_game_end()
                if end is not None:
                    message = "The game has ended and " + end + " has won!"
                    await self.channels["town-of-discord"].send(message)
                    self.started = False
                await self.move(self.bot)
        else:
            print("Game has not started")

    def check_game_end(self):
        """Check to see if the game should end. Returns something if it should end"""
        # End of game condiditons:
        # Mafia wins if there are numMafia >= numTown AND no other evil roles
        # Town wins if all evil roles have been killed
        print(self.characterManager.players)
        numTown = 0
        numMafia = 0
        winner = None
        for player in self.characterManager.players:
            if player.alive == 1:
                if player.role["alignment"] == -1:
                    numMafia += 1
                elif player.role["alignment"] == 1:
                    numTown += 1

        if numMafia >= numTown:
            winner = "Mafia"
        if numMafia == 0:
            winner = "Town"
        return winner


    # @commands.command()
    # async def vote(self, ctx, user):
    #     """Lets Players Leave The Game."""
    #     if ctx.message.author.name in self.players:
    #         message = ctx.message.author.name + "has left the game"
    #         self.players.pop(ctx.message.author.name, None)
    #         await ctx.send(message)
    #     else:
    #         await ctx.send("You are not part of this game.")


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

        if "lobby" in str(channel):
            lobby = channel
            if len(lobby.members) < 1:
                message = "There are not enough players in the game. Please make more friends"
                await ctx.send(message)

            else:
                self.started = True

                makeChannel = True

                makeCategory = True
                for channel in ctx.guild.channels:
                    if gameChannel in str(channel):
                        makeChannel = False
                        break

                for category in ctx.guild.categories:
                    if "Game" in str(category):
                        makeCategory = False
                        break

                if makeCategory is True:
                    self.categories["Game"] = await ctx.guild.create_category_channel("Game")

                if makeChannel is True:
                    await ctx.message.guild.create_voice_channel(gameChannel, category=self.categories["Game"])
                    await ctx.message.guild.create_text_channel("town-of-discord", category=self.categories["Game"])

                for channel in ctx.message.guild.channels:
                    self.channels[channel.name] = channel

                print("These are the available channels:", self.channels)

                for guild in ctx.bot.guilds:
                    # get muted role
                    for role in guild.roles:
                        # print(role)
                        if "muted" in str(role):
                            # print("found muted role")
                            muted = role
                            self.roles["muted"] = muted
                            break
                    break

                await self.channels[gameChannel].set_permissions(muted,
                                                                 connect=False,
                                                                 speak=False,
                                                                 mute_members=False,
                                                                 deafen_members=False)

                # Move members to game channel
                for member in lobby.members:
                    self.players.append(member)
                    await member.move_to(self.channels[gameChannel])

                self.characterManager.initCharacters(self.players)

                print("Players in character manager:", str(self.characterManager.players))
                for player in self.characterManager.players:

                    message = "Hello" + player.member.name + " Welcome to Town of Discord! The game has started. You have the role of:\n ```"
                    #print("blah blah", player.member)
                    message += player.role["name"] + "\n"
                    message += str(player.role["summary"]) + "\n"
                    message += str(player.role["goal"]) + "\n"
                    message += str(player.role["attributes"]) + "\n"
                    message += str(player.alive) + "```\n"
                    await player.member.send(message)

                message = "The Game Has Started"
                await ctx.send(message)
                await self.move(self.bot)
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

        #Removes all made categories
        for category in ctx.guild.categories:
            if "game" in str(category).lower():
                print(category)
                await category.delete()
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







