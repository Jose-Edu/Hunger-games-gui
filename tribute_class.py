from random import randint
from random import choice
import funcs


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
        self.inventory = {'weapon': [], 'armor': [], 'tools': [], 'resource': []}
        self.relation = []
        self.location = [3, 3]
        self.actions = 3
        self.trait = choice(('antisocial', 'lucky', 'brawler', 'walker', 'greedy', 'insane', 'survival', 'reliable', 'pacifist', 'paranoid', 'healty', 'natural', 'cruel'))

        for c in range(0, 24):
            self.relation.append(50+randint(-30, 30))
        self.relation[self.id] = 50

        if mode != 'solo':
            if self.id % 2 == 0:
                self.relation[self.id+1] = 100
            else:
                self.relation[self.id-1] = 100


    def move(self, direction = 'logic'):
        moves = self.actions
        
        if moves < 3 and self.trait == 'walker':
            moves += 1
        if direction == 'random':
            for c in range(0, moves):
                ctrl = [False, False]
                while ctrl != [True, True]:
                    r = choice(((1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, -1)))
                    ctrl = [False, False]
                    if self.location[0] + r[0] < 7 and self.location[0] + r[0] > 0:
                        self.location[0] += r[0]
                        ctrl[0] = True
                    if self.location[1] + r[1] < 7 and self.location[1] + r[1] > 0:
                        self.location[1] += r[1]
                        ctrl[1] = True
            self.actions -= moves
            return None
        elif direction == 'logic':
            biomes = {}
            for b in ('m', 'f', 'mr', 'ff', 'ffr', 'plr', 'fqr', 'd', 'p', 'pl'):
                biomes[b] = randint(0, 3)
                if b[-1] == 'r' and self.trait == 'survival':
                    biomes[b] += 2
                if b[-1] == 'r' and self.resource < 50:
                    biomes[b] += 1
            if self.resource < 50:
                biomes['ff'] += 1
                biomes['fqr'] += 1
                if self.resource < 35:
                    biomes['ffr'] += 1
            if self.trait == 'antisocial' or self.trait == 'pacifist':
                biomes['m'] += 1
                biomes['mr'] += 1
            ctrl = 'm'
            for c in biomes.keys():
                if biomes[c] > biomes[ctrl]:
                    ctrl = c
                elif biomes[c] == biomes[ctrl]:
                    ctrl = choice((ctrl, c))
            go_to = funcs.closest_biome(ctrl, self.location)
        else:
            go_to = direction
        if go_to != self.location:
            while self.actions > 0 and go_to != self.location:
                if self.location[0] == go_to[0]:
                    if self.location[1] > go_to[1]:
                        self.location[1] -= 1
                    else:
                        self.location[1] += 1
                    self.actions -= 1
                elif self.location[1] == go_to[1]:
                    if self.location[0] > go_to[0]:
                        self.location[0] -= 1
                    else:
                        self.location[0] += 1
                    self.actions -= 1
                elif self.location[0] > go_to[0]:
                    self.location[0] -= 1
                    if self.location[1] > go_to[1]:
                        self.location[1] -= 1
                    else:
                        self.location[1] += 1
                    self.actions -= 1
                else:
                    self.location[0] += 1
                    if self.location[1] > go_to[1]:
                        self.location[1] -= 1
                    else:
                        self.location[1] += 1
                    self.actions -= 1


    def update(self, tributes):
        self.actions = 3
        self.resource -= 5
        if self.resource <= 0:
            self.vigour -= 5
            self.sanity -= 5
            if self.trait == 'paranoid': self.sanity -= 5
            elif self.trait == 'healty': self.vigour += 2
        for c in (self.resource, self.vigour, self.sanity):
            if c < 0:
                c = 0
        for c in range(0, 24):
            if c != self.id and tributes[c].vigour > 0:
                distance = funcs.get_distance(self.location, tributes[c].location)
                dif = (12, 8, 4, -4, -8, -12, -16)[distance]
                sign = 1
                if self.relation[c] < 50: sign = -1
                if dif > 0:
                    self.relation[c] += dif*sign
                else:
                    if sign == 1:
                        if self.relation[c]-sign*dif < 50:
                            self.relation[c] = 50
                        else:
                            self.relation[c] -= dif*sign
                    else:
                        if self.relation[c]-sign*dif > 50:
                            self.relation[c] = 50
                        else:
                            self.relation[c] -= dif*sign           


    def combat(self, other_one):
        s_atk = self.power - other_one.resistence + randint(0, 20)
        o_atk = other_one.power - self.resistence + randint(0, 20)

        if self.trait == 'brawler':
            s_atk += 5
        if other_one.trait == 'brawler':
            o_atk += 5

        if o_atk > s_atk:
            self.vigour = 0
            other_one.vigour -= s_atk
            other_one.sanity -= 30
            return False
        else:
            other_one.vigour = 0
            self.vigour -= o_atk
            self.sanity -= 30
            self.actions -= 1
            if self.trait == 'paranoid':
                self.sanity -= 10
            return True


    def items(self, i=None):
        if i == None:
            item = funcs.get_item(self.inventory)
        else:
            item = i
        self.inventory[item['type']].append(item)
        if 'power' in item.keys():
            self.power += item['power']
        if 'resistence' in item.keys():
            self.resistence += item['resistence']
        return item['name']


    def remove_item(self, item):
        self.inventory[item['type']].remove(item)
        if 'power' in item.keys():
            self.power -= item['power']
        if 'resistence' in item.keys():
            self.resistence -= item['resistence']
        return item['name']


    def steal_items(self, t):
        for c in t.inventory.keys():
            for i in t.invetory[c]:
                if i not in self.inventory[c] or i['name'] in ('Explosivo', 'Veneno', 'Kit médico', 'Kit de suprimentos'):
                    self.inventory[c].append(i)
                    self.items(i)
                    t.remove_item(i)


    def have_item(self, item):
        if item in self.inventory['weapon'] or item in self.inventory['armor'] or item in self.inventory['tools'] or item in self.inventory['resource']:
            return True
        else:
            return False


    def biome(self, mode=None):
        _map = funcs.world_map()
        if mode == None:
            location = _map[self.location[0]][self.location[1]]
            return location
        elif mode == 'r':
            location = _map[self.location[0]][self.location[1]]
            if location[-1] == 'r':
                return True
            else:
                return False
        

    def action(self, event, main):
        try_count = 0

        while True:
            if self.actions > 0:
                if event == 'O banho de sangue':
                    ac = randint(0, 3)
                    if ac == 0: # fugir da cornocópia
                        self.move()
                        return {'format': '1', 'text': f'{self.name} fugiu da cornocópia', 'extra_tributes': ()}
                    elif ac == 1: # mina terrestre
                        bonus = 0
                        if self.trait == 'walker' or self.trait == 'paranoid':
                            bonus += 1
                        elif self.trait == 'lucky' or self.trait == 'survival':
                            bonus += 2
                        
                        if bonus + randint(0, 3) > 2 or try_count > 100:
                            self.vigour = 0
                            main.round_deaths += 1
                            return {'format': '1', 'text': f'{self.name} morreu pisando numa mina terrestre', 'extra_tributes': ()}
                        else:
                            try_count += 1
                    elif ac == 2: #pegar item e sair
                        bonus = 0
                        if self.trait in ('greedy', 'lucky'):
                            bonus += 1
                        if bonus + randint(0, 3) > 1 or try_count > 100:
                            item = self.items()
                            self.actions -= 1
                            self.move()
                            return {'format': '1', 'text': f'{self.name} pegou um(a) {item} e saiu do centro', 'extra_tributes': ()}
                        else:
                            try_count += 1
                    elif ac == 3: # matar por item
                        bonus = 0
                        if self.trait in ('greedy', 'brawler', 'cruel'):
                            bonus += 1
                        if bonus + randint(0, 3) >= 2 or try_count > 100:
                            t = funcs.find_tribute(main.tributes, self.id, 'e', 0)
                            c = self.combat(main.tributes[t])
                            if c:
                                it = self.items()
                                return {'format': '2', 'text': f'{self.name} matou {main.tributes[t].name} disputando um(a) {it}', 'extra_tributes': (t)}
                            else:
                                it = main.tributes[t].items()
                                return {'format': '2', 'text': f'{main.tributes[t].name} matou {self.name} disputando um(a) {it}', 'extra_tributes': (t)}
                        else:
                            try_count += 1
                
                elif event == '' and main.time == 'Dia':

                    if randint(0, 1) == 1 or try_count > 100:
                        if self.vigour < 50 or self.resource < 50 == 1:
                            ac = randint(0, 4)
                            
                            if ac == 0:#pescar
                                if self.have_item('Kit de pesca') or self.have_item('Lança'):
                                    if self.biome('r'):
                                        self.resource += 30
                                        self.actions -= 1
                                        return {'format': '1', 'text': f'{self.name} pescou', 'extra_tributes': ()}
                                    else:
                                        try_count += 1
                                else:
                                    try_count += 1
                            
                            if ac == 1:#colher frutos
                                if self.biome() in ('ff', 'ffr', 'fqr'):
                                    self.resource += 15
                                    self.sanity += 5
                                    self.actions -= 1
                                    return {'format': '1', 'text': f'{self.name} Colheu frutos', 'extra_tributes': ()}
                                else:
                                    try_count += 1
                            
                            if ac == 2:#esplorar a arena
                                self.move()
                                return {'format': '1', 'text': f'{self.name} explorou a arena', 'extra_tributes': ()}
                            
                            if ac == 3:#buscar recurso com aliado

                                t = funcs.find_tribute(main.tributes, self.id, 'f', 0)

                                main.tributes[t].resource += 20
                                self.resource += 20
                                
                                main.tributes[t].relation[self.id] += 20
                                self.relation[t] += 20

                                return {'format': '2', 'text': f'{self.name} e {main.tributes[t].name} buscam recursos juntos.', 'extra_tributes': (t)}

                            if ac == 4:#atacar de arco ou 38
                                if self.have_item('Arco e flecha') or self.have_item('38'):
                                    bonus = 0
                                    if self.trait in ('brawler', 'insane', 'cruel', 'greedy'):
                                        bonus += 1
                                    elif self.trait == 'pacifist':
                                        bonus -= 2
                                    if bonus + randint(0, 3) > 2 or try_count > 100:
                                        
                                        if self.have_item('38'):
                                            weapon = '38'
                                        else:
                                            weapon = 'Arco e flecha'
                                        
                                        if self.trait in ('survival', 'brawler'):
                                            bonus = 1
                                        else:
                                            bonus = 0
                                        
                                        t = funcs.find_tribute(main.tributes, self.id, 'e', 1)

                                        if bonus + randint(0, 4) >= 2:
                                            self.sanity -= 20
                                            if self.trait == 'paranoid': self.sanity -= 10
                                            main.tributes[t].vigour = 0
                                            main.round_deaths += 1
                                            return {'format': '2', 'text': f'{self.name} caçou e matou {main.tributes[t].name} usando um {weapon}.', 'extra_tributes': (t)}
                                        else:
                                            self.sanity -= 5
                                            if self.trait == 'paranoid': self.sanity -= 5
                                            self.relation[t] -= 20
                                            main.tributes[t].relation[self.id] -= 40
                                            return {'format': '2', 'text': f'{self.name} tentou caçar {main.tributes[t].name} usando um {weapon}, mas falhou.', 'extra_tributes': (t)}
                                    else:
                                        try_count += 1
                                else:
                                    try_count += 1
                        
                        else:
                            try_count += 1
                    
                    bonus = 0
                    
                    if self.trait == 'insane': bonus += 1
                    
                    if self.sanity < 50 and randint(0, 1) + bonus >= 1:
                        ac = randint(0, 4)
                        
                        if ac == 0:#trair aliado
                            t = funcs.find_tribute(main.tributes, self.id, 'f', 0)
                            r = self.combat(main.tributes[t])
                            if r: return {'format': '2', 'text': f'{self.name} caçou e matou {main.tributes[t].name}.', 'extra_tributes': (t)}
                            else: return {'format': '2', 'text': f'{self.name} morreu tentando caçar {main.tributes[t].name}.', 'extra_tributes': (t)}

                        if ac == 1:#explodir alguém
                            if self.have_item('Explosivo'):
                                t = funcs.find_tribute(main.tributes, self.id, 'e', 0)
                                self.remove_item({'name': 'Explosivo', 'type': 'tools'})
                                self.sanity -= 25
                                main.tributes[t].vigour = 0
                                main.round_deaths += 1
                                return {'format': '2', 'text': f'{self.name} explodiu {main.tributes[t].name}.', 'extra_tributes': (t)}
                            else:
                                try_count += 1
                        
                        if ac == 2:#caçar alguém
                            t = funcs.find_tribute(main.tributes, self.id, 'e', 0)
                            r = self.combat(main.tributes[t])
                            if r: return {'format': '2', 'text': f'{self.name} caçou e matou {main.tributes[t].name}.', 'extra_tributes': (t)}
                            else: {'format': '2', 'text': f'{self.name} morreu tentando caçar {main.tributes[t].name}.', 'extra_tributes': (t)}

                        if ac == 3:#deixar de confiar em todos
                            for c in self.relation:
                                c = 0
                            return {'format': '1', 'text': f'{self.name} deixou de confiar nos outros.', 'extra_tributes': ()}
                        
                        if ac == 4:#deixar de confiar em alguém
                            t = funcs.find_tribute(main.tributes, self.id, 'f')
                            self.relation[t] -= 35
                            self.sanity -= 10
                            if self.trait == 'paranoid': 
                                self.relation[t] -= 15
                                self.sanity -= 5
                            return {'format': '2', 'text': f'{self.name} perdeu a sua confiança em {main.tributes[t].name}.', 'extra_tributes': (t)}

                        if ac == 5:#suícidio
                            self.vigour = 0
                            main.round_deaths += 1
                            return {'format': '1', 'text': f'{self.name} não aguentou as circunstâncias e cometeu suícidio.', 'extra_tributes': ()}

                    elif self.sanity < 50:
                        ac = randint(0, 1)
                        
                        if ac == 0:#pegar flores
                            if self.biome() in ('pl', 'plr'):
                                self.sanity += 8
                                return {'format': '1', 'text': f'{self.name} colheu flores no campo.', 'extra_tributes': ()}
                            else:
                                try_count += 1

                        if ac == 1:#passar um tempo com um amigo
                            t = funcs.find_tribute(main.tributes, self.id, 'f', 0)
                            self.relation[t] += 20
                            main.tributes[t].relation[self.id] += 8
                            if main.tributes[t].trait == 'reliable': self.relation[t] += 18
                            return {'format': '2', 'text': f'{self.name} passou um tempo com {main.tributes[t].name}.', 'extra_tributes': (t)}
                    
                    else:
                        ac = randint(0, 9)
                        
                        if ac == 0:#receber item
                            b = 0
                            if self.trait == 'lucky': b += 1
                            if randint(0, 4) >= 2:
                                i = self.items()
                                return {'format': '1', 'text': f'{self.name} recebeu um(a) {i} de um patrocinador desconhecido.', 'extra_tributes': ()}
                            else:
                                try_count += 1
                        
                        if ac == 1:#morrer imbecilmente
                            kill = [
                                f'{self.name} morreu de desinteria.',
                                f'{self.name} morreu caindo num buraco.'
                            ]
                            if self.biome() == 'ffr': kill.append(f'{self.name} morreu caindo num rio congelado.')
                            if self.biome() in ('ff', 'fqr', 'ffr'): 
                                kill.append(f'{self.name} morreu por comer frutos venenosos.')
                                kill.append(f'{self.name} morreu caindo de uma árvore.')
                            kill = choice(kill)
                            self.vigour = 0
                            main.round_deaths += 1
                            return {'format': '1', 'text': kill, 'extra_tributes': ()}
                        
                        if ac == 2:#envenenar alguém
                            if self.have_item('Veneno'):
                                bonus = 0
                                main.round_deaths += 1
                                if self.trait == 'lucky': bonus += 1
                                if bonus + randint(0, 4) >= 2 or try_count > 100:
                                    self.remove_item({'name': 'Veneno', 'type': 'tools'})
                                    t = funcs.find_tribute(main.tributes, self.id, 'e', 0)
                                    main.tributes[t].vigour = 0
                                    self.sanity -= 15
                                    return {'format': '2', 'text': f'{self.name} envenenou a comida de {main.tributes[t].name}, matando-o', 'extra_tributes': (t)}
                                else:
                                    t = funcs.find_tribute(main.tributes, self.id, 'e', 0)
                                    main.tributes[t].sanity -= 10
                                    self.vigour = 0
                                    return {'format': '2', 'text': f'{self.name} envenenou a comida de {main.tributes[t].name}, mas acabou comendo-a por engano, assim, morrendo.', 'extra_tributes': (t)}
                            else:
                                try_count += 1
                        
                        if ac == 3:#ouvir conversa
                            t1 = funcs.find_tribute(main.tributes, self.id, 'e', 2)
                            t2 = funcs.find_tribute(main.tributes, t1, 'f', 0, [self.id])
                            self.sanity -= 5
                            if self.trait == 'paranoid': self.sanity -= 10
                            main.tributes[t1].relation[t2] += 10
                            main.tributes[t2].relation[t1] += 10
                            self.relation[t1] -= 5
                            self.relation[t2] -= 10

                        if ac == 4:#malhar
                            self.power += 8
                            self.actions -= 1
                            self.sanity += 3
                            return {'format': '1', 'text': f'{self.name} ficou malhando o dia todo.', 'extra_tributes': ()}

                        if ac == 5:#caçar alguém
                            bonus = -2 if self.trait == 'pacifist' else 0
                            if bonus + randint(0, 4) >= 2 or try_count > 100:
                                t = funcs.find_tribute(main.tributes, self.id, 'e', 1)
                                self.move(main.tributes[t].location)
                                r = self.combat(main.tributes[t])
                                if r:
                                    return {'format': '2', 'text': f'{self.name} caçou e matou {main.tributes[t].name}.', 'extra_tributes': (t)}
                                else:
                                    return {'format': '2', 'text': f'{self.name} morreu tentando caçar {main.tributes[t].name}.', 'extra_tributes': (t)}
                            else:
                                try_count += 1
                        
                        if ac == 6:#explorar a arena
                            self.move()
                            return {'format': '1', 'text': f'{self.name} explorou a arena.', 'extra_tributes': ()}

                        if ac == 7:#caçar de arco ou 38
                            if self.have_item('Arco e flecha') or self.have_item('38'):
                                bonus = 0
                                if self.trait in ('brawler', 'insane', 'cruel', 'greedy'):
                                    bonus += 1
                                elif self.trait == 'pacifist':
                                    bonus -= 2
                                if bonus + randint(0, 3) > 2 or try_count > 100:
                                    
                                    if self.have_item('38'):
                                        weapon = '38'
                                    else:
                                        weapon = 'Arco e flecha'
                                    
                                    if self.trait in ('survival', 'brawler'):
                                        bonus = 1
                                    else:
                                        bonus = 0
                                    
                                    t = funcs.find_tribute(main.tributes, self.id, 'e', 1)

                                    if bonus + randint(0, 4) >= 2:
                                        self.sanity -= 20
                                        if self.trait == 'paranoid': self.sanity -= 10
                                        main.tributes[t].vigour = 0
                                        main.round_deaths += 1
                                        return {'format': '2', 'text': f'{self.name} caçou e matou {main.tributes[t].name} usando um {weapon}.', 'extra_tributes': (t)}
                                    else:
                                        self.sanity -= 5
                                        if self.trait == 'paranoid': self.sanity -= 5
                                        self.relation[t] -= 20
                                        main.tributes[t].relation[self.id] -= 40
                                        return {'format': '2', 'text': f'{self.name} tentou caçar {main.tributes[t].name} usando um {weapon}, mas falhou.', 'extra_tributes': (t)}
                                else:
                                    try_count += 1
                            else:
                                try_count += 1
                        
                        if ac == 8:#criar inimizade
                            bf = funcs.find_tribute(main.tributes, self.id, 'bf')
                            t = funcs.find_tribute(main.tributes, self.id, 'random', 0, [bf])
                            print('8 ok')

                            self.relation[t] -= 20
                            main.tributes[t].relation[self.id] -= 15
                            for c in (self.relation[t], main.tributes[t].relation[self.id]):
                                c -= 10 if self.trait == 'paranoid' else 0

                            return {'format': '2', 'text': f'{self.name} discutiu intensamente com {main.tributes[t].name} numa disbuta territorial.', 'extra_tributes': (t)}

                        if ac == 9:#fazer uma lança
                            bonus = 1 if self.trait == 'survival' else 0
                            if bonus + randint(0, 4) >= 2 or try_count > 100:
                                self.items({'name': 'Lança', 'type': 'weapon', 'power': 40})
                                self.sanity += 5
                                return {'format': '1', 'text': f'{self.name} fabricou uma lança.', 'extra_tributes': ()}
                            else:
                                try_count += 1

                elif event == '' and main.time == 'Noite':
                    ac = 0
                    
                    if ac == 0:#fazer uma barraca
                        bonus = 0
                        bonus += 1 if self.trait == 'survival' else 0
                        bonus += 2 if self.have_item({'name': 'Kit de acampamento', 'type': 'tools'}) else 0

                        if bonus + randint(0, 4) >= 2:
                            self.sanity += 10
                            self.vigour += 10
                            return {'format': '1', 'text': f'{self.name} montou um acampamento para dormir.', 'extra_tributes': ()}
                        else:
                            self.sanity -= 10
                            self.vigour -= 5
                            return {'format': '1', 'text': f'{self.name} falhou em montar um acampamento e dormiu no frio.', 'extra_tributes': ()}
                    
                    if ac == 1:#dormir em outro acampamento
                        pass
                    #roubar
                    #envenenar alguém
                    #brigar com alguém
                    #pensar em casa
                    #explodir acampamento
                    #chorar até dormir
                    #tratar ferimentos de aliado
                    #caçar de arco e flecha


            else:
                self.actions = 3
                return {'format': '1', 'text': f'{self.name} descansou.', 'extra_tributes': ()}

