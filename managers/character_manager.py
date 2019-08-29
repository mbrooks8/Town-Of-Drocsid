import logging
from models import Character
import random
log = logging.getLogger('tod')


class CharaterManager():
    """Tracks the number of posts people make."""
    log.debug("character class made")

    def getRoles(self, count):
        if count < 1:
            return[]
        civilianCount = count - 2 - round(count/4)#removes the doctor and detective and the mafia members
        mafiaCount = round(count/4)
        detectiveCount = 1
        doctorCount = 1
        roles ={
            "civilianCount":civilianCount,
            "mafiaCount":mafiaCount,
            "detectiveCount":detectiveCount,
            "doctorCount":doctorCount
            };
        print("count is: ",count)
        return roles
    
    def initCharacters(self, memberList):
        print(memberList)
        players = []
        roles = self.getRoles(len(memberList))
        print(roles)
        if roles is []:
            return False
        for member in memberList:
            sample = random.sample(roles.items(), k=1)
            print(sample)
            alignment = 0 
            role = 0
            summary = ""
            abilities = ""
            attributes = ""
            goal = ""
            players.append(Character(member, alignment, role, summary, abilities, attributes, goal))

            
        if len(memberList)%4 == 0:
            print("the ideal size")
        else:
            print("you can still play, but the 3:1 ratio is off")
        return True
    
