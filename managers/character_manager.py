import logging
from models import Character
from models import Role
import random
import json
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
        #update roles to store a usable Role class
        roles["civilian"]["count"] = civilianCount
        roles["mafia"]["count"] = mafiaCount
        roles["doctor"]["count"] = doctorCount
        roles["detective"]["count"] = detectiveCount
        return roles
    
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

        # for player in self.players:
        #     print(player)
            
        if len(memberList) % 4 == 0:
            print("the ideal size")
        else:
            print("you can still play, but the 3:1 ratio is off")
        return True
    
