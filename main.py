"""
Arquivo principal do projeto, define a janela e funções básicas e importa o restante do conteúdo.
Execute este arquivo para inicializar o App.
"""


#Importação das bibliotecas e funções usadas
import tkinter as gui #Interface gráfica
from windows import * #Importa as classes referentes às diferentes possíveis telas do programa
from os.path import dirname #Importa a função usada para a leitura do diretório atual


class window_base:

    """Cria a classe base do projeto."""

    #Configurações básicas da janela do programa: Tamanho, título, ícone e etc.
    app = gui.Tk()
    app.title('Hunger Games GUI')
    app.iconbitmap('images//common//ico.ico')
    app.geometry('800x600')
    app.resizable(False, False)
    bg_cl = '#8B0000'
    frame = gui.Frame(app, background=bg_cl)
    frame.pack(fill='both', expand='yes')
    menu = gui.Menu(app)


    def __init__(self):

        """
        Classe base do projeto.\n\n
        Configurações de inicialização:
            * Define a janela do programa;
            * Importa telas;
            * Declara variáveis de controle;
            * Cria o menu.
        """

        #Importação das diferentes telas
        self.mm = main_menu(self)
        self.st = show_tributes(self)
        self.game = game(self)
        self.mm.exec()
        self.ws = win_screen(self)
        self.ts = transition_screen(self)

        #Declaração das variáveis de controle
        self.tributes = []
        self.menu = gui.Menu(self.app)
        self.day = 1
        self.time = 'Dia'
        self.game_mode = ''
        self.round_deaths = 0

        #Criação do menu
        self.menu = gui.Menu(self.app)
        menu_actions = gui.Menu(self.menu, tearoff=0)
        menu_actions.add_command(label='Map', command=self.open_map)
        menu_actions.add_command(label='Tributes Info', command=self.open_tributes_info)
        self.menu.add_cascade(label='Actions', menu=menu_actions)


    def reset_window(self):

        """Função que limpa a tela do programa, destruindo o Frame atual e criando um novo."""

        self.frame.destroy()
        self.frame = gui.Frame(self.app, background=self.bg_cl)
        self.frame.pack(fill='both', expand='yes')


    def open_map(self):

        """Função que abre a tela secundária do mapa."""

        path = dirname(__file__)
        exec(open(path+'\\map.py').read(), {'bg_cl': self.bg_cl, 'path': path, 'tributes': self.tributes})


    def open_tributes_info(self):

        """Função que abre a tela secundária das informações dos tributos."""

        path = dirname(__file__)
        exec(open(path+'\\tributes_info.py').read(), {'bg_cl': self.bg_cl, 'path': path, 'tributes': self.tributes}) 


    def tributes_count(self):
        
        """Função que retorna o número atual de tributos restantes no jogo."""

        t_count = 24

        for c in self.tributes:
            if c.vigour < 1:
                t_count -= 1

        return t_count


    def day_update(self):
        
        """Função que atualiza o horário e, consequentemente, o contador de dias.\n\nRedefine as configurações para o próximo dia."""

        if self.time == 'Dia':
            self.time = 'Noite'
        else:
            self.time = 'Dia'
            self.day += 1
        self.round_deaths = 0
        for t in self.tributes:
            t.update(self.tributes)


#Atribuição da classe e estrutura básica de Apps Tkinter
_global_ = window_base()
_global_.app.mainloop()