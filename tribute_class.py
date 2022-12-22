from random import randint
from random import choice


class tribute:
    def __init__(self, name, id, img_25, img_100, img_200, mode):
        self.name = name
        self.id = id
        self.img_25px = img_25
        self.img_100px = img_100
        self.img_200px = img_200
        self.vigour = 100 + randint(-15, 30)
        self.resource = 100 - randint(0, 60)
        self.power = 15 + randint(-10, 10)
        self.resistence = 0 + randint(-5, 5)
        self.sanity = 100 - randint(0, 30)
        self.inventory = {'weapons': [], 'armor': [], 'tools': [], 'resource': []}
        self.relation = []
        self.location = [3, 3]
        self.actions = 3
        self.trait = choice(('antisocial', 'lucky', 'brawler', 'walker', 'greedy', 'insane', 'survival', 'reliable', 'pacifist', 'paranoid', 'healty', 'natural'))

        for c in range(0, 24):
            self.relation.append(50+randint(-10, 10))
        self.relation[self.id] = 50

        if mode != 'solo':
            if self.id % 2 == 0:
                self.relation[self.id+1] = 100
            else:
                self.relation[self.id-1] = 100