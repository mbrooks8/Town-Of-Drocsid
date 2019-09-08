# Town-Of-Drocsid

Cool Bot for Town Of Salem

## Setup

#### Install Requirements:
```
pip install -r requirements.txt
```

#### Setup SecretKey:
```
create file named "secretkey.txt" in root directory of project and copy and paste the API key in the file
```

#### Run the bot:

    run bot.py

## Game
When the bot runs, it will create a voice and text channel for the lobby. All of the players in the lobby will be waiting for the game to start.

Start the game by typing in the lobby:

    !start

Once the command is sent, the game will automatically start and roles will be assigned. Phases of the game move automatically on a set timer.

The phases of the game are:

        Night: Lock chat channel and mute voice channel
        Discussion: open voice channel unlock chat channel
        Judgement: mute all players except the voted player and block everyone from posting in chat channel except the voted player