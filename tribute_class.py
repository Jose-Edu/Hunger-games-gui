from random import randint


class tribute:
    def __init__(self, name, id, img_25, img_100, img_200):
        self.name = name
        self.id = id
        self.img_25px = img_25
        self.img_100px = img_100
        self.img_200px = img_200
        self.vigour = 100 + randint(-30, 30)
        self.resource = 100 - randint(0, 60)
        self.power = 30 + randint(-10, 10)
        self.resistence = 0 + randint(-5, 5)
        self.sanity = 100 - randint(0, 30)
        self.inventory = {'weapons': [], 'armor': [], 'tools': [], 'resource': []}
        self.relation = []
        self.location = [3, 3]
        self.allies = []
        self.enemies = []