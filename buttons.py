import funcs
from tribute_class import tribute
import os

def bt_main_menu(mode, game_mode, tributes, frame):
    game_mode.append(mode)
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

    formats = funcs.images_set()
    imgs = {'25': [], '100': [], '200': []}

    for c in ('25', '100', '200'):
        path_imgs = path+f'\\temp\\{c}px\\'
        for i in range(1, 25):
            imgs[c].append(path_imgs+str(i)+formats[c][i-1])

    for c in range(0, 24):
        tributes.append(tribute(names[c], c, imgs['25'][c], imgs['100'], imgs['200'], mode))
