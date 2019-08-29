class Character(object):
    def __init__(self, member, alignment, role, summary, abilities, attributes, goal, alive =1):
        self.member = member
        self.role = role
        self.alignment = alignment

        self.summary = summary
        self.abilities = abilities
        self.attributes = attributes
        self.goal = goal

        self.alive = alive

    def setRole(self, role):
        self.role = role

    def setAlignment(self, alignment):
        self.alignment = alignment

    def setSummary(self, summary):
        self.summary = summary

    def setAbilities(self, abilities):
        self.abilities = abilities

    def setAttributes(self, attributes):
        self.attributes = attributes

    def setGoal(self, goal):
        self.goal = goal

    def setAlive(self, alive):
        self.alive = alive