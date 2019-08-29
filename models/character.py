class Character(object):
    def __init__(self, member, alignment, role, alive =1):
        self.member = member
        self.role = role
        self.alignment = alignment
        self.alive = alive

    def setRole(self, role):
        self.role = role

    def setAlignment(self, alignment):
        self.alignment = alignment

    def setAlive(self, alive):
        self.alive = alive