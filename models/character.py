class Character(object):
    def __init__(self, name, role, alive):
        self.name = name
        self.role = role
        self.alive = alive

    def setName(self, name):
        self.name = name

    def setRole(self, role):
        self.role = role

    def setAlive(self, alive):
        self.alive = alive
