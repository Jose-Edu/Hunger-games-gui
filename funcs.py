import shutil, os
from PIL import Image
from tribute_class import tribute


def repeat(value, number):
    l = []
    for c in range(0, number):
        l.append(value)
    return l


def world_map():
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
    m[4][0], m[4][1], m[5][0], m[5][1], m[5][2], m[6][0], m[6][1], m[6][2] = repeat('pr', 8)
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