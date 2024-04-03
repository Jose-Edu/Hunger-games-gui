"""
Arquivo que definine funções próprias do projeto.
(Doc wip) 
"""


#Importações das bibliotecas e funções usadas
import os #Biblioteca usada para fuções operacionais (Manipular pastas e arquivos)
from shutil import copy #Importa a função de copiar arquivos para outro diretório
from PIL import Image #Importa a função de manipular imagens
from tribute_class import tribute #Importa a classe que define os tributos
from random import randint, choice #Importa as funções aleatórias de: número inteiro aleatório e escolha aleatória


def repeat(value, number):

    """Função que cria uma lista que repete o valor "value" "number" vezes. Retorna a lista."""

    l = []
    for c in range(0, number):
        l.append(value)
    return l


def world_map():

    """
    Função que define retorna a matriz de biomas do mapa do jogo.\n
    Legenda dos biomas:
    * m = montanha;
    * f = feast;
    * mr montanha com rio;
    * ff = floresta fria;
    * ffr = floresta fria com rio;
    * plr = planicie com rio;
    * fqr = floresta quente com rio;
    * d = deserto;
    * p = pântano;
    * pl = planicie.
    """

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

    """
    Função que define as imagens dos tributos,\n 
    adicionando as enviadas pelo usuário e colocando genéricas quando nescessário.\n
    Retorna um dicionário com todas as extenções das imagens, para facilitar consultas.
    """

    #Armazena o caminho do arquivo na variável path
    path = os.path.dirname(__file__)

    #Cria o dicionário que guardará as extenções dos arquivos
    formats = {'25': [], '100': [], '200': []}

    #Caso ainda não exista, cria as pastas de imagens temporárias
    if not os.path.exists(path+'\\images\\temp'):
        os.mkdir(path+'\\images\\temp')
        os.mkdir(path+'\\images\\temp\\25px')
        os.mkdir(path+'\\images\\temp\\100px')
        os.mkdir(path+'\\images\\temp\\200px')

    #Laço principal que acha os arquivo os move às pastas certas, transformando suas resoluções
    for c in range(1, 25): # c = Tributo atual do laço

        #Define o suposto caminho da imagem, sem sua extensão
        origin = path+f'\\images\\tributes\\{c}'

        #Procura a extensão da imagem entre as opções aceitas e, ao achar, salva esse dado no formats.
        for t in ('.png', '.jpg', '.jpeg', '.gif'):
            if os.path.exists(origin+t):
                for size in ('25', '100', '200'):
                    formats[size].append(t)
                
                #Aplica a extenção do arquivo nas vars que armazenam os paths
                origin += t
                destiny = path+f'\\images\\temp\\sizepx\\{c}{t}'
                break

        try: #Copia os arquivos para as pastas certas e redefine suas resoluções
            
            for size in ('25', '100', '200'):
                des = destiny.replace('size', size)
                copy(origin, des)
                img = Image.open(des)
                _img = img.resize((int(size), int(size)))
                _img.save(des)

        except: #Se o usuário não definir uma imagem, resultará em erro. Nesse caso, o except usará uma imagem genérica
            for size in ('25', '100', '200'):
                origin = path+f'\\images\\common\\t{size}px.gif'
                destiny = path+f'\\images\\temp\\{size}px\\{c}.gif'
                formats[size].append('.gif')
                copy(origin, destiny)

    #Se a imagem não salva em '.png' ou '.gif', trasforma as suas copias em '.png'
    for size in ('25', '100', '200'):
        for c in range(1, 25):

            if formats[size][c-1] not in ('.png', '.gif'):

                p = path+f'\\images\\temp\\{size}px\\{c}{formats[size][c-1]}'
                i = Image.open(p)
                i.save(path+f'\\images\\temp\\{size}px\\{c}.png')
                os.remove(p)
                formats[size][c-1] = '.png'

    #Retorna a lista de extenções
    return formats


def tributes_create(mode, tributes):

    """
    Função que cria cada um dos 24 tributos e armazena-os no argumento tributes.
    """

    #Armazena o caminho das imagens
    path = os.path.dirname(__file__)+'\\images'

    # region nomes

    #Cria a lista de nomes
    names = []
    n_file = open(path+'\\tributes\\tributes.txt', 'rt')

    #Lê os nomes e os armazena na lista
    for c in range(0, 24):
        names.append(n_file.readline())

    n_file.close()

    #Executa uma limpa no texto do nome, tirando espaços incorretos, quebra de linhas e adiciona nome genérico quando nescessário
    for c in range(0, 24):

        names[c] = names[c].strip()

        if names[c] == '' or names[c] == '\n':
            names[c] = 'T'+str(c+1)

        if names[c][(len(names[c])-3):] == '\n':
            names[c] = names[c][:(len(names[c])-3)]
    # endregion

    # region imagens

    #Define os arquivos das imagens e define variáveis de controle
    formats = images_set()
    imgs = {'25': [], '100': [], '200': []}

    #Armazena os paths de cada uma das imagens no dict imgs
    for c in ('25', '100', '200'):
        path_imgs = path+f'\\temp\\{c}px\\'
        for i in range(1, 25):
            imgs[c].append(path_imgs+str(i)+formats[c][i-1])
    # endregion

    #Cria cada um dos tributos
    for c in range(0, 24):
        tributes.append(tribute(names[c], c, imgs['25'][c], imgs['100'][c], imgs['200'][c], mode))


def get_biome_locate(biomes):

    """Função que retorna uma lista com todos pontos do mapa que sejam de um dos biomas passados.\n
        biomes = lista de biomas com nomes conforme definido em world_map()
    """

    #Definições
    wm = world_map()
    locations = []

    #Checa célula por célula da matriz e, quando achar biomas corretos, adiciona a localização à lista locations
    for l in range(0, 7): #l = Linha atual do laço
        for c in range(0, 7): #c = Coluna atual do laço
            if str(wm[l][c]) in biomes:
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
    ctrl = get_biome_locate((biome))[0]
    for b in get_biome_locate((biome)):
        if get_distance(locate, b) < get_distance(locate, ctrl):
            ctrl = b
        elif get_distance(locate, b) == get_distance(locate, ctrl):
            ctrl = choice((ctrl, b))
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
        it = choice(it)
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
            t = randint(0, 23)
            if _tributes[t].vigour > 0 and t != _self and distance >= get_distance(_tributes[_self].location, _tributes[t].location) and t not in exceptions: break

        return t
    if mode == 'f':
        t = []
        for c in range(0, 23):
            if _tributes[c].vigour > 0 and c != _self and distance >= get_distance(_tributes[_self].location, _tributes[c].location) and c not in exceptions:
                if _tributes[_self].relation[c] >= 50:
                    t.append(c)
        try:
            return choice(t)
        except:
            return find_tribute(_tributes, _self, 'random', distance)
    elif mode == 'e':
        t = []
        for c in range(0, 23):
            if _tributes[c].vigour > 0 and c != _self and distance >= get_distance(_tributes[_self].location, _tributes[c].location) and c not in exceptions:
                if _tributes[_self].relation[c] < 50:
                    t.append(c)
        try:
            return choice(t)
        except:
            return find_tribute(_tributes, _self, 'random', distance)
    elif mode == 'bf':
        t = 0
        for c in range(0, 23):
            if _tributes[c].vigour > 0 and c != _self and distance >= get_distance(_tributes[_self].location, _tributes[c].location) and c not in exceptions:
                if _tributes[_self].relation[c] > _tributes[_self].relation[t]:
                    t = c
                elif _tributes[_self].relation[c] == _tributes[_self].relation[t]:
                    t = choice((t, c))
        return t
    elif mode == 'we':
        t = 0
        for c in range(0, 23):
            if _tributes[c].vigour > 0 and c != _self and distance >= get_distance(_tributes[_self].location, _tributes[c].location) and c not in exceptions:
                if _tributes[_self].relation[c] < _tributes[_self].relation[t]:
                    t = c
                elif _tributes[_self].relation[c] == _tributes[_self].relation[t]:
                    t = choice((t, c))
        return t
    
