"""
Arquivo que carrega as diferentes telas, dividas por classes, usadas pela windou_base de main.py
"""

#Importações de bibliotecas e funções usadas
import tkinter as gui #Interface gráfica
from tkinter.ttk import Scrollbar #Importa a função de barra de rolagem da interface gráfica
import funcs #Importa as funções próprias do projeto
from os.path import dirname #Importa a função usada para a leitura do diretório atual


#Configuração da tela de menu principal
class main_menu:


    #Importa o main, permitindo a ligação com a window_base
    def __init__(self, main):
        self.main = main


    #Limpa a tela e gera o menu principal
    def exec(self):
        self.main.reset_window()
        
        title = gui.Label(self.main.frame, text = 'Hunger Games GUI', foreground='#000', font=('Algerian', 48), background=self.main.bg_cl)
        title.pack()

        bt_solo = gui.Button(self.main.frame, text='Solo', command= lambda: self.main.st.exec('solo'))
        bt_solo.place(width=100,height=50, x = 400, y = 350, anchor='center')
        bt_districts = gui.Button(self.main.frame, text='Districts', command= lambda: self.main.st.exec('districts'))
        bt_districts.place(width=100,height=50, x = 400, y = 450, anchor='center')
        bt_classic = gui.Button(self.main.frame, text='Classic', command= lambda: self.main.st.exec('classic'))
        bt_classic.place(width=100,height=50, x = 400, y = 550, anchor='center')

        path = dirname(__file__)
        img = gui.PhotoImage(file=path+'\\images\\common\\logo.png')
        img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
        img_label.photo = img
        img_label.pack()

        self.main.world_map = funcs.world_map()


#Configuração da tela que mostra os tributos participantes
class show_tributes:


    #Importa o main, permitindo a ligação com a window_base
    def __init__(self, main):
        self.main = main


    #Configura as definições básicas do jogo, limpa a tela e cria a tela que mostra os tributos participantes
    def exec(self, game_mode):

        #Definições gerais: Aplica o menu, define o modo de jogo e cria os tributos
        self.main.app.config(menu=self.main.menu)
        self.main.game_mode = game_mode
        funcs.tributes_create(game_mode, self.main.tributes)

        #Limpa a tela
        self.main.reset_window()


        # region Criação e configuração da barra de rolagem
        
        #Cria um canvas dentro do Frame principal
        my_canvas = gui.Canvas(self.main.frame)
        my_canvas.pack(side='left', fill='both', expand='yes')

        #Cria a barra de rolagem
        scroll = Scrollbar(self.main.frame, orient='vertical', command=my_canvas.yview)
        scroll.pack(side='right', fill='y')

        #Configura o canvas para usar a barra de rolagem
        my_canvas.configure(yscrollcommand=scroll.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox('all')))

        
        #Função que faz a barra de rolagem poder ser usada pela roda do mouse
        def _on_mouse_wheel(event):
            try:
                my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
            except:
                pass
        

        #Aplica a função no canvas
        my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

        #Cria um frame dentro do canvas para ser o conteúdo que seguirá a barra de rolagem
        frame = gui.Frame(my_canvas)
        my_canvas.create_window((0,0), window=frame, anchor='nw', width=800, height=1253)
        frame.configure(background=self.main.bg_cl)
        # endregion


        #Título da página
        title = gui.Label(frame, text = 'Tributes', foreground='#000', font=('Algerian', 48), background=self.main.bg_cl)
        title.pack()


        # region Laço para a criação do layout dos tributos, determina a linha
        for l in range(0, 24, 4): #l = linha atual do laço (de 4 em 4, para acompanhar os tributos)

            #Laço para fazer cada um dos tributos
            for c in range(0, 4): #c = coluna atual do laço

                #Chega se o jogo está no modo Solo, para criar, ou não, a legenda dos distritos
                if game_mode != 'solo' and c % 2 == 0:
                    if c == 0:
                        num = 1
                    else:
                        num = 2
                    text = gui.Label(frame, text=f'District {int(l/2+num)}', font=('Arial Black', 14), background='#000', foreground='#fff')
                    text.place(x=52+c*200, y=115+l/4*190, width=300)
                
                #Aplica a imagem do tributo atual do laço
                img = gui.PhotoImage(file=self.main.tributes[l+c].img_100px)
                img_label = gui.Label(frame, image=img, background=self.main.bg_cl)
                img_label.photo = img
                img_label.place(x=50+c*200,y=150+l/4*190)

                #Escreve o nome do tributo atual do laço
                if self.main.tributes[l+c].vigour > 0: #Caso esteja vivo, a cor do texto é verde
                    cl = '#228c22'
                else:
                    cl = '#000' #Caso esteja morto, a cor do texto é preto
                gui.Label(frame, text=self.main.tributes[l+c].name, font=('Arial Black', 10), background='#fff', foreground=cl).place(x=102+c*200,y=262+l/4*190, width=160, height=20, anchor='center')
        # endregion
        
        
        #Botão 'Next' que leva para a tela de simulação
        bt_next = gui.Button(frame, text='Next', command=self.main.game.exec, width=20)
        bt_next.pack(side='bottom')


#Configuração da tela de simulação
class game:

    #Variável que controla o id dos tributos, avançando de 1 em 1, passando por todos, assim, permitindo todas as ações
    tb_ac = -1

    #Importa o main, permitindo a ligação com a window_base
    def __init__(self, main):
        self.main = main


    #Cria a tela de simulação
    def exec(self, event=None):


        def tributes_actions():

            """Função que limpa a tela, executa a ação do tributo (tribute[x]).action())\n
              e cria o layout demostrativo a partir do dicionário de retorno de action()\n
              É aplicado no botão 'Next' gerado na mesma página e no botão 'Next' da tela show_tributes."""

            #Limpa a tela e avança o tb_ac
            self.main.reset_window()
            self.tb_ac += 1

            #Laço que pula o turno de todos os tributos que já agiram fora de hora ou que estão mortos
            while self.tb_ac < 24:

                if self.main.tributes[self.tb_ac].vigour < 1 and self.main.tributes[self.tb_ac].actions > 0:
                    self.tb_ac += 1

                else:
                    break
            
            #Checa se o tb_ac chegou ao limite e, se sim, termina a rodada executando a tela de transição. 
            if self.tb_ac == 24:
                self.main.ts.exec()

            #Se ainda houver tributos para simular, executa o turno
            else:

                #Simula a ação do tributo atual e armazena o retorno na var turn_print
                turn_print = self.main.tributes[self.tb_ac].action(event, self.main)
                #turn_print = {'format': '1', 'text': 'Text', 'extra_tributes': ()}

                #Cria o título e o subtítulo (subtítulo = turn_print['text'])
                title = gui.Label(self.main.frame, text = f'{self.main.time} {self.main.day}:', foreground='#000', font=('Algerian', 48), background=self.main.bg_cl)
                title.pack()

                subtitile = gui.Label(self.main.frame, text = turn_print['text'], foreground='#000', font=('Book Antiqua', 12), background=self.main.bg_cl)
                subtitile.pack()

                # region Definição da próxima tela e do botão do botão 'Next'
                #Se houver apenas um tributo vivo e o modo de jogo não for por distritos, ele é o vencedor.
                #Armazena o vencedor na var winner e a função de executar a tela de vitória no botão 'Next'.
                if self.main.game_mode != "districts" and self.main.tributes_count() == 1:
                    for c in range(0, 24):
                        if self.main.tributes[c].vigour > 0:
                            winner = c
                            break
                    bt_next = gui.Button(self.main.frame, text='Next', command=lambda:self.main.ws.exec(winner))
                
                #Se só houver dois tributos vivos e o jogo estiver no modo de distritos, checa possível vitória.
                elif self.main.tributes_count() < 3 and self.main.game_mode == 'districts':

                    #Se só houver um tributo vivo, busca o distrito vencedor e aplica a execução da tela de vitória no botão 'Next'.
                    if self.main.tributes_count() == 1:

                        #Checa qual o é o tributo vivo
                        for c in range(0, 24):
                            if self.main.tributes[c].vigour > 0:
                                winner = c+1
                                break
                        
                        #Checa se o tributo vivo é o primeiro ou segundo do distrito, assim armazenado a ordem e tributos corretos
                        r = []
                        if winner % 2 != 0:
                            dist = int((winner+1)/2)
                            r.append(winner-1)
                            r.append(winner)
                        else:
                            dist = int((winner)/2)
                            r.append(winner)
                            r.append(winner+1)

                        r.append(dist)
                        bt_next = gui.Button(self.main.frame, text='Next', command=lambda:self.main.ws.exec(r))

                    #Se o jogo ainda não tiver um vencedor, checa se ainda há tributos na rodada, definindo a próxima tela do botão 'Next'.
                    else:

                        tbs = []

                        for c in range(0, 24): #Checa quais são os tributos vivos
                            if self.main.tributes[c].vigour > 0:
                                tbs.append(c)
                        
                        if tbs[1] == tbs[0] + 1: #Se for um distrito
                            dist = int((tbs[1]+1)/2)
                            r = (tbs[0], tbs[1], dist)
                            bt_next = gui.Button(self.main.frame, text='Next', command=lambda:self.main.ws.exec(r))

                        else: #Se não, decide se segue as checagens ou se vai para a tela de transição
                            if self.tb_ac < 23:
                                bt_next = gui.Button(self.main.frame, text='Next', command=tributes_actions)
                            else:
                                bt_next = gui.Button(self.main.frame, text='Next', command=self.main.ts.exec)
                
                #Se não houver nenhum tributo vivo, aplica no botão 'Next' a execução da tela de empate.
                elif self.main.tributes_count() == 0:
                    bt_next = gui.Button(self.main.frame, text='Next', command=lambda:self.main.ws.exec(-1))

                #Se o jogo ainda não tiver um vencedor, checa se ainda há tributos na rodada, definindo a próxima tela do botão 'Next'.
                else:
                    if self.tb_ac < 23:
                        bt_next = gui.Button(self.main.frame, text='Next', command=tributes_actions)
                    else:
                        bt_next = gui.Button(self.main.frame, text='Next', command=self.main.ts.exec)
                
                #Posiciona o botão que executa a próxima tela
                bt_next.place(x = 400, y = 550, anchor = 'center', width=100, height=50)
                # endregion

                # region Leitura e execução do layout utilizado (layout = turn_print['format'])

                if turn_print['format'] == '1':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 400, y = 300, anchor = 'center')

                if turn_print['format'] == '2':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes']].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')

                if turn_print['format'] == '3':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 150, y = 300, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][0]].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 400, y = 300, anchor = 'center')
                    
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][1]].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 650, y = 300, anchor = 'center')

                if turn_print['format'] == '2x2':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 400, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][2]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 400, anchor = 'center')

                if turn_print['format'] == '2x1':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 400, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][1]].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')
                
                if turn_print['format'] == '1x2':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 400, anchor = 'center')
                
                if turn_print['format'] == '3x1':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 450, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][2]].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')
                
                if turn_print['format'] == '1x3':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][2]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 450, anchor = 'center')

                if turn_print['format'] == '3x2':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 450, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][2]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][3]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 400, anchor = 'center')

                if turn_print['format'] == '2x3':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 400, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][2]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][3]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 450, anchor = 'center')

                if turn_print['format'] == '3x3':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 450, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][2]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][3]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[turn_print['extra_tributes'][4]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 450, anchor = 'center')
                
                # endregion
        
        #Limpa a tela e redefine o tb_ac
        self.main.reset_window()
        self.tb_ac = -1

        #Cria o título da página
        title = gui.Label(self.main.frame, text = f'{self.main.time} {self.main.day}:', foreground='#000', font=('Algerian', 48), background=self.main.bg_cl)
        title.pack()

        #Caso não haja um evento predefinido, define o evento (wip)
        if event == None:
            if self.main.day == 1 and self.main.time == 'Dia':
                event = 'O banho de sangue'
#            elif self.main.day % 3 == 0 and  and not self.main.day % 5 == 0 and self.main.time == 'Dia':
#                event = 'Feast'
#            elif self.main.day % 5 == 0:
#                if choice((True, False)):
#                    event = 'event' #ph
#                else:
#                    event = ''
            else:
                event = ''

        #Se o evento não for um dia ou noite padrão, cria um subtítulo com o nome do evento
        if event != '':
            subtitile = gui.Label(self.main.frame, text = event, foreground='#000', font=('Arial Black', 22), background=self.main.bg_cl)
            subtitile.pack()
        
        #Define o texto mostrado na tela para cada evento
        if event == '' and self.main.time == 'Dia':
            text = 'O dia amanhece normalmente'
        elif event == '':
            text = 'O sol se pôs e a noite se iniciou'
        elif event == 'O banho de sangue':
            text = 'Os tributos sobem em seus pódios e a buzina soa'
        else:
            text = ''

        #Aplica o texto do evento na tela
        text_label = gui.Label(self.main.frame, text=text, foreground='#000', font=('Book Antiqua', 14), background=self.main.bg_cl)
        text_label.place(x = 400, y = 300, anchor='center')

        #Aplica o botão 'Next' que executa a tela de simulação
        bt_next = gui.Button(self.main.frame, text='Next', command=tributes_actions)
        bt_next.place(x = 400, y = 550, anchor = 'center', width=100, height=50)


#Configuração da tela final de vitória ou empate
class win_screen:

    #Importa o main, permitindo a ligação com a window_base
    def __init__(self, main):
        self.main = main


    #Limpa a tela, fecha o menu e mostra o resultado final da simulação
    def exec(self, winner):

        #Limpa a tela e destrói o menu
        self.main.reset_window()
        self.main.menu.destroy()

        # region Tela de empate
        if winner == -1: #Se não houver vencedor

            #Título
            title = gui.Label(self.main.frame, text='O Hunger Games terminou em empate!', font=('Algerian', 22), foreground= '#000', background=self.main.bg_cl)
            title.pack()

            #Botão 'Return' que reinicia o programa
            bt_return = gui.Button(self.main.frame, text='Return', command=self.main.__init__)
            bt_return.place(x = 400, y = 550, anchor = 'center', width = 100, height = 50)
        # endregion

        # region Tela de vitória
        else: #Caso haja um vencedor ou distrito vencedor
            
            #Tela de vencedor individual
            if self.main.game_mode != 'districts': #Se o modo de jogo não for de distritos

                #Título
                title = gui.Label(self.main.frame, text=f'{self.main.tributes[winner].name}\né o(a) vencedor(a) do Hunger Games!', font=('Algerian', 22), foreground= '#000', background=self.main.bg_cl)
                title.pack()

                #Imagem do Tributo
                img = gui.PhotoImage(file=self.main.tributes[winner].img_200px)
                img_label = gui.Label(self.main.frame, image=img, border=False, borderwidth=0, background=self.main.bg_cl)
                img_label.photo = img
                img_label.place(x = 400, y = 300, anchor = 'center')

                #Botão "Return" que reinicia o programa
                bt_return = gui.Button(self.main.frame, text='Return', command=self.main.__init__)
                bt_return.place(x = 400, y = 550, anchor = 'center', width = 100, height = 50)

            #Tela de distrito vencedor
            else: #Se o modo de jogo for de distritos
                
                #Título
                title = gui.Label(self.main.frame, text=f'O distrito {winner[2]} é o vencedor do Hunger Games!', font=('Algerian', 22), foreground= '#000', background=self.main.bg_cl)
                title.pack()

                #Imagens dos dois tributos
                img = gui.PhotoImage(file=self.main.tributes[winner[0]].img_200px)
                img_label = gui.Label(self.main.frame, image=img, border=False, borderwidth=0, background=self.main.bg_cl)
                img_label.photo = img
                img_label.place(x = 200, y = 300, anchor = 'center')

                img = gui.PhotoImage(file=self.main.tributes[winner[1]].img_200px)
                img_label = gui.Label(self.main.frame, image=img, border=False, borderwidth=0, background=self.main.bg_cl)
                img_label.photo = img
                img_label.place(x = 600, y = 300, anchor = 'center')

                #Botão "Return" que reinicia o programa
                bt_return = gui.Button(self.main.frame, text='Return', command=self.main.__init__)
                bt_return.place(x = 400, y = 550, anchor = 'center', width = 100, height = 50)
        # endregion


#Configuração da tela de transição
class transition_screen:

    #Importa o main, permitindo a ligação com a window_base
    def __init__(self, main):
        self.main = main


    #Limpa a tela e mostrar a mensagem de fim de dia e contador de mortes (se houver mortes)
    def exec(self):

        #Limpa a tela
        self.main.reset_window()

        #Se houver mortes no dia, cria a tela
        if self.main.round_deaths > 0:
            
            #Título
            title = gui.Label(self.main.frame, text= f'Fim do(a) {self.main.time.lower()} {self.main.day}:', font=('Algerian', 48), background=self.main.bg_cl)
            title.pack()

            #Texto do contador de mortes
            text = gui.Label(self.main.frame, text=f'{self.main.round_deaths} disparo(s) de canhão pode(m) ser ouvidos à distância', font=('Book Antiqua', 12), background=self.main.bg_cl)
            text.place(x=400, y=300, anchor='center')

            #Botão "Next" que leva para a tela de mostrar os tributos
            bt_next = gui.Button(self.main.frame, text= 'Next', command= lambda: self.main.st.exec(self.main.game_mode))
            bt_next.place(x=400, y=600, anchor='s', width=100, height=50)

            #Executa o Day_update()
            self.main.day_update()

        #Se não houver mortes, pula a tela de transição
        else:
            self.main.day_update()
            self.main.st.exec(self.main.game_mode)

