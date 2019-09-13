import discord
from managers import character_manager 
from discord.ext import commands
from datetime import datetime, timedelta
import time
import asyncio
import operator



phases = {
    "night":0,
    "discussion":1,
    "night":2,
}
class GameManager(commands.Cog):
    """Manages the game."""
    # Phases of the game are:
    # night -- 0
    # discussion & voting -- 1
    # Judgement -- 2
    def __init__(self, bot):
        self.bot = bot
        self.gameIsRunning = False
        self.characterManager = character_manager.CharaterManager()
        self.phase = 0
        self.client = discord.Client()
        self.roles = {}
        self.channels = {}
        self.categories = {}
        self.lobby = {}
        self.firstTurn = True

    async def start_timer(self, delay, what):
        """Starts a await sleep timer. Lets you do run a function and let other people still send commands"""
        if self.gameIsRunning is True:
            await self.channels["gameTextChannel"].send(what)
            await asyncio.sleep(delay - 5)
            await self.channels["gameTextChannel"].send("Phase is ending in 5 seconds")
            await asyncio.sleep(5)

    async def move(self, ctx):
        """Moves the phase of the game to the next phase."""
        if self.gameIsRunning is True:
            self.phase = (self.phase + 1) % 3
            print("The current phase is:", self.phase)
            voteMessage = self.characterManager.getVoteList()
            if self.phase == 0:
                self.characterManager.clearVotes()
                # Night
                # regular town people move to individual channels
                for player in self.characterManager.players:
                    # mafia move to a group channel with all mafia members
                    if player.role["alignment"] == -1:
                        print(self.channels)
                        message = "its time to kill someone... vote for them\n"
                        await player.textChannel.send(message+voteMessage)
                        await player.member.move_to(self.channels["Mafia"])
                    else:
                        await player.member.move_to(player.voiceChannel)

                    # doctor is given a list of people to heal, doctor picks one
                    if player.role["name"] == "Doctor":
                        message = "its time to save someone... vote for them\n"
                        await player.textChannel.send(message+voteMessage)

                    # detective is given a list of people to investigate, detective picks one and their role is revealed
                    if player.role["name"] == "Detective":
                        message = "its time to investigate someone... vote for them\n"
                        await player.textChannel.send(message+voteMessage)


                loop = asyncio.get_event_loop()
                task1 = loop.create_task(self.start_timer(20, '```\n🌃 🌃 Night Phase Has Started 🌃 🌃\n```'))
                await task1
                await self.move(self.bot)

            if self.phase == 1:
                # Discussion:
                if self.firstTurn is not True:
                    mafiaVote = self.characterManager.getElected("Mafia")
                    doctorVote = self.characterManager.getElected("Doctor")
                    detectiveVote = self.characterManager.getElected("Detective")
                    if detectiveVote != None: 
                        for player in self.characterManager.players:
                            if player.role["name"] == "Detective":
                                message = "they are a "+detectiveVote.role["name"]+"\n"
                                await player.textChannel.send(message+voteMessage)
                    if mafiaVote != None:
                        if mafiaVote is doctorVote:
                            await self.channels["town-of-drocsid"].send("Doctor has saved "+str(mafiaVote.member))
                        else:
                            message = "Mafia has killed "+str(mafiaVote.member)
                            if doctorVote != None:
                                message += ", and the doctor sucks... they tried to save "+ str(doctorVote.member)
                            await self.channels["town-of-drocsid"].send(message)
                            print("mafia killed", mafiaVote)
                            print("doctor sucks, they saved ", doctorVote)
                    self.characterManager.clearVotes()

                    print("Trying to move players to main channel")
                    for player in self.characterManager.players:
                        print("Moving", player.member.name)
                        try:
                            await player.member.move_to(self.channels["gameVoiceChannel"])
                        except Exception as e:
                            print(e)
                # day lasts for 45 seconds
                loop = asyncio.get_event_loop()
                task1 = loop.create_task(self.start_timer(10, '\n 👯 👯 Discussion Phase Has Started 👯 👯\n'))
                await task1
                await self.move(self.bot)

            if self.phase == 2:
                # Judgement
                if self.firstTurn is not True:
                    # TODO: call Vote function
                    townVote = self.characterManager.getElected()
                    if townVote != None:
                        townVote.kill()
                    messaage = "The town killed ", townVote
                    await self.channels["gameTextChannel"].send(messaage)
                    # Judgement: mute all players except the voted player
                    # and block everyone from posting in chat channel except the voted player

                    # TODO: call Vote function

                    loop = asyncio.get_event_loop()
                    task1 = loop.create_task(self.start_timer(5, '\n 👮 👮 Judgement Phase Has Started 👮 👮\n'))
                    await task1

                    winner = self.check_game_end()
                    if winner is not None:
                        # The game is over
                        # Send end game messaage to channel
                        message = "🎆 🎆 🎆 The game has ended and " + winner + " has won 🎆 🎆 🎆!"
                        await self.channels["gameTextChannel"].send(message)
                        self.gameIsRunning = False
                self.firstTurn = False
                await self.move(self.bot)
        else:
            print("Game has not started")

    def check_game_end(self):
        """Check to see if the game should end. Returns something if it should end"""
        numTown = 0
        numMafia = 0
        winner = None
        for player in self.characterManager.players:
            if player.isAlive():
                if player.role["alignment"] == -1:
                    numMafia += 1
                elif player.role["alignment"] == 1 or player.role["alignment"] == 2:
                    numTown += 1

        if numMafia >= numTown:
            winner = "Mafia"
        if numMafia == 0:
            winner = "Town"
        return winner
    
    @commands.command()
    async def vote(self, ctx, *args):
        """Lets Players Vote For Something."""
        for player in self.characterManager.players:
            if str(player.member) == str(ctx.message.author):
                if player.isAlive:
                    index = int(args[0])
                    player.vote = index
                    await player.textChannel.send("you voted for: "+str(self.characterManager.players[index].member) )
                    print(str(player.member), " voted for ", self.characterManager.players[index].member)

    @commands.command()
    async def start(self, ctx, *args):
        """Starts the game."""
        playerList = []
        gameChannel = "Town of Drocsid"
        self.phase = 0
        channel = ctx.message.author.voice.channel

        if "lobby" in str(channel):
            lobby = channel
            if len(lobby.members) < 1:
                message = "There are not enough players in the game. Please make more friends"
                await ctx.send(message)

            else:
                self.gameIsRunning = True
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
                    mainGameChannel = await ctx.message.guild.create_voice_channel(gameChannel, category=self.categories["Town Of Drocsid"])
                    self.channels["gameVoiceChannel"] = mainGameChannel
                    mainTextChannel = await ctx.message.guild.create_text_channel("town-of-drocsid", category=self.categories["Town Of Drocsid"])
                    self.channels["gameTextChannel"] = mainTextChannel

                # print("These are the available channels:", self.channels)

                # get all of the roles
                for guild in ctx.bot.guilds:
                    for role in guild.roles:
                        self.roles[str(role)] = role

                await self.channels["gameVoiceChannel"].set_permissions(self.roles["muted"], connect=False, speak=False, mute_members=False, deafen_members=False)

                # Move members to game channel
                for member in lobby.members:
                    playerList.append(member)
                    await self.channels["gameVoiceChannel"].join()
                    # TODO: Have the bot join the main channel
                    await member.move_to(self.channels["gameVoiceChannel"])

                # Assign game roles to each person in the game
                self.characterManager.initCharacters(playerList)

                # Create channel for Mafia:
                mafiaChannel = await ctx.message.guild.create_voice_channel("Mafia", category=self.categories["Town Of Drocsid"])
                mafiaText = await ctx.message.guild.create_voice_channel("MafiaText", category=self.categories["Town Of Drocsid"])
                await mafiaChannel.set_permissions(ctx.message.guild.default_role, read_messages=False)
                await mafiaText.set_permissions(ctx.message.guild.default_role, read_messages=False)
                self.channels["Mafia"] = mafiaChannel
                self.channels["MafiaText"] = mafiaChannel

                # Create indiviual channels for each player and then send them a message about their roles
                for player in self.characterManager.players:
                    await self.createIndividualChannel(player, ctx.message.guild)
                    await self.sendGameStartMessage(player)

                message = "The Game Has Started"
                await self.channels["gameTextChannel"].send(message)
                await self.move(self.bot)
        else:
            message = "You must be in the lobby to start the game"
            await ctx.send(message)

    async def createIndividualChannel(self, player, guild):
        # TODO Need to create these channels in a different order or using less api calls.
        channelName = str(player.member)
        voice = await guild.create_voice_channel(channelName, category=self.categories["Town Of Drocsid"])
        text = await guild.create_text_channel(channelName, category=self.categories["Town Of Drocsid"])
        player.voiceChannel = voice
        player.textChannel = text

        await voice.set_permissions(player.member, read_messages=True)
        await voice.set_permissions(guild.default_role, read_messages=False)
        await text.set_permissions(player.member, read_messages=True)
        await text.set_permissions(guild.default_role, read_messages=False)

        if player.role["alignment"] == -1:
            # player is mafia, create a channel for all of the mafia members and let them be in there
            await self.channels["Mafia"].set_permissions(player.member, read_messages=True)
            await self.channels["MafiaText"].set_permissions(player.member, read_messages=True)

    async def sendGameStartMessage(self, player):
        message = "Hello " + player.member.name + \
                  " Welcome to Town of Drocsid!\n" \
                  "The game has started. You have the role of:```"
        message += "Name: " + str(player.role["name"]) + "\n\n"
        message += "Summary: " + str(player.role["summary"]) + "\n\n"
        message += "Goal: " + str(player.role["goal"]) + "\n\n"
        message += "Attributes: " + str(player.role["attributes"]) + "```\n"

        if player.role["alignment"] == -1:
            # player is a mafia, they need to know all the other mafia members
            message += "As a member of the mafia, your mafia mates are:\n```\n"
            for mafiaPlayer in self.characterManager.players:
                if mafiaPlayer.role["alignment"] == -1:
                    message += mafiaPlayer.member.name + "\n"
            message += "```\n Good Luck!"
        await player.textChannel.send(message)

    @commands.command()
    async def end(self, ctx, *args):
        """Forces the game to end."""
        channel = ctx.message.channel
        if "lobby" in str(channel):
            self.gameIsRunning = False
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
            message = "The Game Has Been Forcefully Stopped by " + ctx.message.author.name
            await ctx.send(message)
        else:
            await ctx.send("You have to send this message in the lobby")


    @commands.command()
    async def moveAll(self, ctx, *args):
        """Moves everyone to channel."""
        channel = ctx.message.channel
        if "lobby" in str(channel):
            for channel in ctx.guild.channels:
                if "lobby" in str(channel):
                    lobby = channel
                    break
            print(ctx.guild.members)
            for member in ctx.guild.members:
                print("Moving user to lobby")
                await member.move_to(lobby)
        else:
            await ctx.send("You have to send this message in the lobby")

    @commands.command()
    async def leave(self, ctx, *args):
        """Lets Players Leave The Game."""
        channel = ctx.message.channel
        if "town-of-drocsid" in str(channel):
            if ctx.message.author.name in self.characterManager.players:
                message = ctx.message.author.name + "has left the game"
                self.players.pop(ctx.message.author.name, None)
                await ctx.send(message)
            else:
                await ctx.send("You are not part of this game.")
        else:
            await ctx.send("You have to send this message in town-of-drocsid")

    @commands.command()
    async def players(self, ctx, *args):
        """Lists the players."""
        channel = ctx.message.channel
        if "town-of-drocsid" in str(channel):
            message = "```These are the players:\n"
            for player in self.characterManager.players:
                message += player.member.name + "\n"
            message += "```"
            await ctx.send(message)
        else:
            ctx.send("You have to send this message in town-of-drocsid")





