from random import randint


class tribute:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.vigour = 100 + randint(-30, 30)
        self.resource = 100 - randint(0, 60)
        self.power = 30 + randint(-10, 10)
        self.resistence = 0 + randint(-5, 5)
        self.sanity = 100 - randint(0, 30)
        self.inventory = {'weapons': [], 'armor': [], 'tools': []}
        self.relation = []
        self.location = [3, 3]
        self.allies = []
        self.enemies = []