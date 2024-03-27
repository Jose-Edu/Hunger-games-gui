import shutil, os
from PIL import Image
from tribute_class import tribute
import random


def repeat(value, number):
    l = []
    for c in range(0, number):
        l.append(value)
    return l


def world_map():

    #m = montanha
    #f = feast
    #mr montanha com rio
    #ff = floresta fria
    #ffr = floresta fria com rio
    #plr = planicie com rio
    #fqr = floresta quente com rio
    #d = deserto
    #p = pântano
    #pl = planicie

    m = []
    for c in range(0, 7):
        m.append([0, 0, 0, 0, 0, 0, 0])
    
    m[0][0] = 'm'
    m[3][3] = 'f'
    m[0][1], m[1][0] = repeat('mr', 2)
    m[0][2], m[1][1], m[2][0] = repeat('ff', 3)
    m[1][2], m[2][1], m[3][0], m[3][1] = repeat('ffr', 4)
    m[2][3], m[3][2], m[3][4], m[4][3] = repeat('plr', 4)
    m[4][5], m[5][4], m[5][6], m[6][3], m[6][5] = repeat('fqr', 5)
    m[0][4], m[0][5], m[0][6], m[1][5], m[1][6], m[2][6] = repeat('d', 6)
    m[4][0], m[4][1], m[5][0], m[5][1], m[5][2], m[6][0], m[6][1], m[6][2] = repeat('p', 8)
    m[0][3], m[1][3], m[1][4], m[2][2], m[2][4], m[2][5], m[3][5], m[3][6], m[4][2], m[4][4] = repeat('pl', 10)

    return m


def images_set():
    path = os.path.dirname(__file__)
    formats = {'25': [], '100': [], '200': []}

    for r in ('25', '100', '200'):
        for c in range(1, 25):
            origin = path+f'\\images\\tributes\\{c}'
            destiny = path+f'\\images\\temp\\{r}px\\{c}'
            for t in ('.png', '.jpg', '.jpeg', '.gif'):
                if os.path.exists(origin+t):
                    origin += t
                    destiny += t
                    formats[r].append(t)
                    break
            try:
                shutil.copyfile(origin, destiny)
            except:
                origin = path+f'\\images\\common\\t{r}px.gif'
                destiny = path+f'\\images\\temp\\{r}px\\{c}.gif'
                formats[r].append('.gif')
                shutil.copyfile(origin, destiny)
            img = Image.open(destiny)
            _img = img.resize((int(r), int(r)))
            _img.save(destiny)
    for r in ('25', '100', '200'):
        for c in range(1, 25):
            if formats[r][c-1] != '.png' and formats[r][c-1] != '.gif':
                p = path+f'\\images\\temp\\{r}px\\{c}{formats[r][c-1]}'
                i = Image.open(p)
                i.save(path+f'\\images\\temp\\{r}px\\{c}.png')
                os.remove(p)
                formats[r][c-1] = '.png'
    return formats


def tributes_create(mode, tributes):
    path = os.path.dirname(__file__)+'\\images'

    names = []
    n_file = open(path+'\\tributes\\tributes.txt', 'rt')
    for c in range(0, 24):
        names.append(n_file.readline())
    n_file.close()
    for c in range(0, 24):
        names[c] = names[c].strip()
        if names[c] == '' or names[c] == '\n':
            names[c] = 'T'+str(c+1)
        if names[c][(len(names[c])-3):] == '\n':
            names[c] = names[c][:(len(names[c])-3)]

    formats = images_set()
    imgs = {'25': [], '100': [], '200': []}

    for c in ('25', '100', '200'):
        path_imgs = path+f'\\temp\\{c}px\\'
        for i in range(1, 25):
            imgs[c].append(path_imgs+str(i)+formats[c][i-1])
    for c in range(0, 24):

        tributes.append(tribute(names[c], c, imgs['25'][c], imgs['100'][c], imgs['200'][c], mode))


def get_biome_locate(biome):
    wm = world_map()
    locations = []

    for l in range(0, 7):
        for c in range(0, 7):
            if wm[l][c] == biome:
                locations.append([l, c])

    return locations


def get_distance(dis1, dis2):
    moves = 0
    c1 = []
    c1.append(dis1[0])
    c1.append(dis1[1])
    c2 = dis2

    while c1[0] != c2[0] or c1[1] != c2[1]:
        moves += 1
        if c1[0] == c2[0]:
            if c1[1] > c2[1]:
                c1[1] -= 1
            else:
                c1[1] += 1
        elif c1[1] == c2[1]:
            if c1[0] > c2[0]:
                c1[0] -= 1
            else:
                c1[0] += 1
        elif c1[0] > c2[0]:
            c1[0] -= 1
            if c1[1] > c2[1]:
                c1[1] -= 1
            else:
                c1[1] += 1
        else:
            c1[0] += 1
            if c1[1] > c2[1]:
                c1[1] -= 1
            else:
                 c1[1] += 1       

    return moves


def closest_biome(biome, locate):
    ctrl = get_biome_locate(biome)[0]
    for b in get_biome_locate(biome):
        if get_distance(locate, b) < get_distance(locate, ctrl):
            ctrl = b
        elif get_distance(locate, b) == get_distance(locate, ctrl):
            ctrl = random.choice((ctrl, b))
    return ctrl


def get_item(inv):
    items = {}
    items['Facão'] = {'name': 'Facão', 'type': 'weapon', 'power': 30}
    items['Arco e flecha'] = {'name': 'Arco e flecha', 'type': 'weapon', 'power': 50}
    items['Colete'] = {'name': 'Colete', 'type': 'armor', 'resistence': 50}
    items['Kit médico'] = {'name': 'Kit médico', 'type': 'resource', 'vigour': 50}
    items['Explosivo'] = {'name': 'Explosivo', 'type': 'tools'}
    items['Veneno'] = {'name': 'Veneno', 'type': 'tools'}
    items['Lança'] = {'name': 'Lança', 'type': 'weapon', 'power': 40}
    items['Capacete'] = {'name': 'Capacete', 'type': 'armor', 'resistence': 15}
    items['Kit de suprimentos'] = {'name': 'Kit de suprimentos', 'type': 'resource', 'resource': 50}
    items['Kit de acampamento'] = {'name': 'Kit de acampamento', 'type': 'tools'}
    items['Crossbow'] = {'name': 'Crossbow', 'type': 'weapon', 'power': 60}
    items['38'] = {'name': '38', 'type': 'weapon', 'power': 100}
    items['Par de botas de escalada'] = {'name': 'Par de botas de escalada', 'type': 'tools'}
    items['Cantil'] = {'name': 'Cantil', 'type': 'tools'}
    items['Machado'] = {'name': 'Machado', 'type': 'weapon', 'power': 30}

    while True:
        it = []
        for c in items.keys():
            it.append(c)
        it = random.choice(it)
        if it not in inv[items[it]['type']] or it in ('Explosivo', 'Veneno', 'Kit médico', 'Kit de suprimentos'): break
    it = items[it]
    return it


def find_tribute(_tributes, _self, mode='random', distance=6, exceptions=[]):
    if mode == 'random':
        r = -1
        while True:
            r+=1
            if r == 40:
                r = 0
                distance+=1
            t = random.randint(0, 23)
            if _tributes[t].vigour > 0 and t != _self and distance >= get_distance(_tributes[_self].location, _tributes[t].location) and t not in exceptions: break

        return t
    if mode == 'f':
        t = []
        for c in range(0, 23):
            if _tributes[c].vigour > 0 and c != _self and distance >= get_distance(_tributes[_self].location, _tributes[c].location) and c not in exceptions:
                if _tributes[_self].relation[c] >= 50:
                    t.append(c)
        try:
            return random.choice(t)
        except:
            return find_tribute(_tributes, _self, 'random', distance)
    elif mode == 'e':
        t = []
        for c in range(0, 23):
            if _tributes[c].vigour > 0 and c != _self and distance >= get_distance(_tributes[_self].location, _tributes[c].location) and c not in exceptions:
                if _tributes[_self].relation[c] < 50:
                    t.append(c)
        try:
            return random.choice(t)
        except:
            return find_tribute(_tributes, _self, 'random', distance)
    elif mode == 'bf':
        t = 0
        for c in range(0, 23):
            if _tributes[c].vigour > 0 and c != _self and distance >= get_distance(_tributes[_self].location, _tributes[c].location) and c not in exceptions:
                if _tributes[_self].relation[c] > _tributes[_self].relation[t]:
                    t = c
                elif _tributes[_self].relation[c] == _tributes[_self].relation[t]:
                    t = random.choice((t, c))
        return t
    elif mode == 'we':
        t = 0
        for c in range(0, 23):
            if _tributes[c].vigour > 0 and c != _self and distance >= get_distance(_tributes[_self].location, _tributes[c].location) and c not in exceptions:
                if _tributes[_self].relation[c] < _tributes[_self].relation[t]:
                    t = c
                elif _tributes[_self].relation[c] == _tributes[_self].relation[t]:
                    t = random.choice((t, c))
        return t