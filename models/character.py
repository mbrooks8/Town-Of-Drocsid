class Character(object):
    def __init__(self, member, role, alive=1,vote = -1):
        self.member = member
        self.role = role
        self.alive = alive
        self.vote = vote
        self.will = ""
        self.textChannel = ""
        self.voiceChannel = ""
        self.visited = ""

    def setRole(self, role):
        self.role = role

    def setAlignment(self, alignment):
        self.alignment = alignment

    def setAlive(self, alive):
        self.alive = alive
        
    def __str__(self):
        output = "member: "+str(self.member)
        output += "\nrole: "+str(self.role)
        output += "\nalive: "+str(self.alive)
        return output