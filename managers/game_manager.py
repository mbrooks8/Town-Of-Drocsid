import discord
from managers import character_manager 
from discord.ext import commands
from datetime import datetime, timedelta
import time
import asyncio
import operator


class GameManager(commands.Cog):
    """Manages the game."""
    # Phases of the game are:
    # night -- 0
    # discussion & voting -- 1
    # Judgement -- 2
    def __init__(self, bot):
        self.bot = bot
        self.started = False
        self.characterManager = character_manager.CharaterManager()
        self.phase = 0
        self.client = discord.Client()
        self.roles = {}
        self.channels = {}
        self.categories = {}
        self.lobby = {}

    async def start_timer(self, delay, what):
        """Starts a await sleep timer. Lets you do run a function and let other people still send commands"""
        if self.started is True:
            await self.channels["town-of-drocsid"].send(what)
            await asyncio.sleep(delay)

    async def move(self, ctx):
        """Moves the phase of the game to the next phase."""
        if self.started is True:
            self.phase = (self.phase + 1) % 3
            print("The current phase is:", self.phase)

            if self.phase == 0:
                # Night
                # regular town people move to individual channels
                for player in self.characterManager.players:
                    # mafia move to a group channel with all mafia members
                    if player.role["attribute"] == -1:
                        await player.member.move_to(self.channels["Mafia"])
                    else:
                        await player.member.move_to(self.channels[player.member.name])

                    # doctor is given a list of people to heal, doctor picks one
                    if player.role["name"] == "doctor":
                        print("Do a doctor thing")

                    # detective is given a list of people to investigate, detective picks one and their role is revealed
                    if player.role["name"] == "detective":
                        print("Do a detective thing")

                loop = asyncio.get_event_loop()
                task1 = loop.create_task(self.start_timer(10, 'Night Phase Has Started'))
                await task1
                await self.move(self.bot)

            if self.phase == 1:
                # Discussion: open voice channel unlock chat channel
                # All players talk to eachother n do stuff

                # day lasts for 45 seconds
                loop = asyncio.get_event_loop()
                task1 = loop.create_task(self.start_timer(10, 'Discussion Phase Has Started'))
                await task1
                await self.move(self.bot)

            if self.phase == 2:
                # Judgement
                # TODO: call Vote function

                loop = asyncio.get_event_loop()
                task1 = loop.create_task(self.start_timer(10, 'Judgement Phase Has Started'))
                await task1

                end = self.check_game_end()
                if end is not None:
                    # The game is over
                    # Send end game messaage to channel
                    message = "The game has ended and " + end + " has won!"
                    await self.channels["town-of-drocsid"].send(message)
                    #Set the game to end
                    self.started = False

                await self.move(self.bot)
        # else:
        #     print("Game has not started")

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
                elif player.role["alignment"] == 1 or player.role["alignment"] == 2:
                    numTown += 1

        if numMafia >= numTown:
            winner = "Mafia"
        if numMafia == 0:
            winner = "Town"
        return winner

    def getElected(self):
        elected = {}
        for player in self.characterManager.players:
            key = str(player.vote)
            if key == "-1":
                continue
            if key not in elected: 
                elected.update({key:0})
            elected[key] = elected[key] + 1
        return self.characterManager.players[int(max(elected.items(), key=operator.itemgetter(1))[0])]
    
    @commands.command()
    async def vote(self, ctx, *args):
        """Lets Players Vote For Something."""
        for player in self.characterManager.players:
            if player.member is ctx.message.author:
                #player.vote = self.players[]
                if player.alive == 1:
                    index = int(args[0])
                    player.vote = index
                    print(str(player.member)," voted for ",self.characterManager.players[index].member)

    @commands.command()
    async def leave(self, ctx, *args):
        """Lets Players Leave The Game."""
        if ctx.message.author.name in self.characterManager.players:
            message = ctx.message.author.name + "has left the game"
            self.players.pop(ctx.message.author.name, None)
            await ctx.send(message)
        else:
            await ctx.send("You are not part of this game.")

    @commands.command()
    async def players(self, ctx, *args):
        """Lists the players."""
        message = "```These are the players:\n"
        for player in self.characterManager.players:
            username = player.nick
            if username is None:
                username = player.name
            message += username + "\n"
        message += "```"
        await ctx.send(message)

    @commands.command()
    async def start(self, ctx, *args):
        """Starts the game."""
        playerList = []
        gameChannel = "Town of Drocsid"
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
                    if "Town Of Drocsid" in str(category):
                        self.categories["Town Of Drocsid"] = category
                        makeCategory = False
                        break

                if makeCategory is True:
                    self.categories["Town Of Drocsid"] = await ctx.guild.create_category_channel("Town Of Drocsid")

                if makeChannel is True:
                    await ctx.message.guild.create_voice_channel(gameChannel, category=self.categories["Town Of Drocsid"])
                    await ctx.message.guild.create_text_channel("town-of-drocsid", category=self.categories["Town Of Drocsid"])

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
                    playerList.append(member)
                    await member.move_to(self.channels[gameChannel])

                # Assign game roles to each person in the game
                self.characterManager.initCharacters(playerList)

                # Create channel for Mafia:
                mafiaChannel = await ctx.message.guild.create_voice_channel("Mafia", category=self.categories["Town Of Drocsid"])
                await mafiaChannel.set_permissions(ctx.message.guild.default_role, read_messages=False)

                # Create indiviual channels for each player
                for player in self.characterManager.players:
                    if player.role["alignment"] == -1:
                        # player is mafia, create a channel for all of the mafia members and let them be in there
                        await mafiaChannel.set_permissions(player.member, read_messages=True)
                    else:
                        channelName = str(player.member)
                        print("player", channelName)
                        voice = await ctx.message.guild.create_voice_channel(channelName, category=self.categories["Town Of Drocsid"])
                        text = await ctx.message.guild.create_text_channel(channelName, category=self.categories["Town Of Drocsid"])
                        player.voiceChannel = voice
                        player.textChannel = text

                        await voice.set_permissions(player.member, read_messages=True)
                        await voice.set_permissions(ctx.message.guild.default_role, read_messages=False)
                        await text.set_permissions(player.member, read_messages=True)
                        await text.set_permissions(ctx.message.guild.default_role, read_messages=False)

                print("Players in character manager:", str(self.characterManager.players))
                for player in self.characterManager.players:
                    message = "Hello " + player.member.name + \
                              " Welcome to Town of Drocsid!\n" \
                              "The game has started. You have the role of:```"
                    message += "Name: " + str(player.role["name"]) + "\n\n"
                    message += "Summary: " + str(player.role["summary"]) + "\n\n"
                    message += "Goal: " + str(player.role["goal"]) + "\n\n"
                    message += "Attributes: " + str(player.role["attributes"]) + "```\n"

                    if player.role["alignment"] == -1:
                        #player is a mafia, they need to know all the other mafia members
                        message += "As a member of the mafia, your mafia mates are:\n```"
                        for player in self.characterManager.players:
                            if player.role["alignment"] == -1:
                                message += player.member.name
                        message += "```\n Good Luck!"

                    await player.textChannel.send(message)

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
        channelList = []

        # gets the lobby
        for channel in ctx.guild.channels:
            if "lobby" in str(channel):
                lobby = channel
                break

        # Gets all game created channels
        for channel in ctx.guild.channels:
            try:
                if str(channel.category) == "Town Of Drocsid":
                    channelList.append(channel)
            except:
                pass

        # moves all users to the lobby
        for member in ctx.guild.members:
            if member.voice is not None:
                print("Moving user to lobby")
                await member.move_to(lobby)

        # deletes game channels
        for channel in channelList:
            await channel.delete()
            
        #delete player specific channels
        for player in self.characterManager.players:
            channelName = str(player.member)
            for channel in ctx.message.guild.channels:
                if channel.name == channelName:
                    await channel.delete()

        #Removes all made categories
        for category in ctx.guild.categories:
            if "Town Of Drocsid" in str(category):
                #print(category)
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







