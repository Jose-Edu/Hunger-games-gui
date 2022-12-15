import shutil, os
from PIL import Image


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

    for r in ('25', '100', '200'):
        for c in range(1, 25):
            origin = path+f'\\images\\tributes\\{c}'
            destiny = path+f'\\images\\temp\\{r}px\\{c}'
            for t in ('.png', '.jpg', '.jpeg', '.gif', '.tiff', '.bmp'):
                if os.path.exists(origin+t):
                    origin += t
                    destiny += t
                    break
            try:
                shutil.copyfile(origin, destiny)
            except:
                origin = path+f'\\images\\common\\t{r}px.png'
                destiny = path+f'\\images\\temp\\{r}px\\{c}.png'
                shutil.copyfile(origin, destiny)
            img = Image.open(destiny)
            _img = img.resize((int(r), int(r)))
            _img.save(destiny)