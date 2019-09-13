import logging
from models import Character
from models import Role
import random
import json
import operator
log = logging.getLogger('tod')


class CharaterManager():
    """Tracks the number of posts people make."""
    log.debug("character class made")

    def __init__(self):
        self.players = []

    def getRoles(self, count):
        with open('./models/roles.json', 'r') as f:
            roles = json.load(f)
        # print(roles.keys())
        if count < 1:
            return[]
        civilianCount = count - 2 - round(count/4)#removes the doctor and detective and the mafia members
        mafiaCount = round(count/4)
        detectiveCount = 1
        doctorCount = 1
        # update roles to store a usable Role class
        roles["civilian"]["count"] = civilianCount
        roles["mafia"]["count"] = mafiaCount
        roles["doctor"]["count"] = doctorCount
        roles["detective"]["count"] = detectiveCount
        return roles

    def clearVotes(self):
        for player in self.players:
            player.vote = -1

    def getVoteList(self):
        message = ""
        for i in range(0,len(self.players)):
            message += str(i)+": "+str(self.players[i].member)+"\n"
            print(i)
            print(self.players[i].member.nick,self.players[i].member)
        print(message)
        return message
    def getElected(self, role=None):
        elected = {}
        for player in self.players:
            if role is not None:
                if player.role["name"] != role:
                    continue
            key = str(player.vote)
            if key == "-1":
                continue
            if key not in elected: 
                elected.update({key: 0})
            elected[key] = elected[key] + 1
        if len(elected) == 0:
            print("nobody voted")
            return None
        return self.players[int(max(elected.items(), key=operator.itemgetter(1))[0])]
    
    def initCharacters(self, memberList):
        self.players = []
        roles = self.getRoles(len(memberList))
        if roles is []:
            return False
        for member in memberList:
            sample = random.sample(roles.keys(), k=1)
            # print(sample)
            key = sample[0]
            roles[key]["count"] = roles[key]["count"] - 1 
            self.players.append(Character(member, roles[key]))
            if roles[key]["count"] == 0:
                del roles[key]
            alignment = 0 
            role = 0
            # todo update key to be the role

        return True
