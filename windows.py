import tkinter as gui
from tkinter import ttk as gui_ttk
import funcs
import os
from random import choice


class main_menu:

    def __init__(self, main):
        self.main = main


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
        path = os.path.dirname(__file__)
        img = gui.PhotoImage(file=path+'\\images\\common\\logo.png')
        img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
        img_label.photo = img
        img_label.pack()

        self.main.world_map = funcs.world_map()


class show_tributes:

    def __init__(self, main):
        self.main = main


    def exec(self, game_mode):

        self.main.app.config(menu=self.main.menu)
        self.main.game_mode = game_mode

        funcs.tributes_create(game_mode, self.main.tributes)
        self.main.reset_window()

        my_canvas = gui.Canvas(self.main.frame)
        my_canvas.pack(side='left', fill='both', expand='yes')

        scroll = gui_ttk.Scrollbar(self.main.frame, orient='vertical', command=my_canvas.yview)
        scroll.pack(side='right', fill='y')
        
        my_canvas.configure(yscrollcommand=scroll.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox('all')))
        def _on_mouse_wheel(event):
            try:
                my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
            except:
                pass
        my_canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
        frame = gui.Frame(my_canvas)
        my_canvas.create_window((0,0), window=frame, anchor='nw', width=800, height=1253)
        frame.configure(background=self.main.bg_cl)

        title = gui.Label(frame, text = 'Tributes', foreground='#000', font=('Algerian', 48), background=self.main.bg_cl)
        title.pack()
        for c in range(0, 24, 4):
            for i in range(0, 4):
                if game_mode != 'solo' and i % 2 == 0:
                    if i == 0:
                        num = 1
                    else:
                        num = 2
                    text = gui.Label(frame, text=f'District {int(c/2+num)}', font=('Arial Black', 14), background='#000', foreground='#fff')
                    text.place(x=52+i*200, y=115+c/4*190, width=300)
                
                img = gui.PhotoImage(file=self.main.tributes[c+i].img_100px)
                img_label = gui.Label(frame, image=img, background=self.main.bg_cl)
                img_label.photo = img
                img_label.place(x=50+i*200,y=150+c/4*190)

                if self.main.tributes[c+i].vigour > 0:
                    gui.Label(frame, text=self.main.tributes[c+i].name, font=('Arial Black', 10), background='#fff', foreground='#228c22').place(x=102+i*200,y=262+c/4*190, width=160, height=20, anchor='center')
                else:
                    gui.Label(frame, text=self.main.tributes[c+i].name, font=('Arial Black', 10), background='#fff', foreground='#000').place(x=102+i*200,y=262+c/4*190, width=150, height=20, anchor='center')
        bt_next = gui.Button(frame, text='Next', command=self.main.game.exec, width=20)
        bt_next.pack(side='bottom')


class game:

    tb_ac = -1

    def __init__(self, main):
        self.main = main


    def exec(self, event=None):
        def tributes_actions():
            self.main.reset_window()
            self.tb_ac += 1

            while self.tb_ac < 24:
                if self.main.tributes[self.tb_ac].vigour < 1 and self.main.tributes[self.tb_ac].actions > 0:
                    self.tb_ac += 1
                else:
                    break
            
            if self.tb_ac == 24:
                self.main.ts.exec()

            else:
                stuff = self.main.tributes[self.tb_ac].action(event, self.main)
                #stuff = {'format': '1', 'text': 'Text', 'extra_tributes': ()}

                title = gui.Label(self.main.frame, text = f'{self.main.time} {self.main.day}:', foreground='#000', font=('Algerian', 48), background=self.main.bg_cl)
                title.pack()
                subtitile = gui.Label(self.main.frame, text = stuff['text'], foreground='#000', font=('Book Antiqua', 12), background=self.main.bg_cl)
                subtitile.pack()

                if self.main.game_mode != "districts" and self.main.tributes_count() == 1:
                    for c in range(0, 24):
                        if self.main.tributes[c].vigour > 0:
                            winner = c
                            break
                    bt_next = gui.Button(self.main.frame, text='Next', command=lambda:self.main.ws.exec(winner))
                elif self.main.tributes_count() < 3 and self.main.game_mode == 'districts':
                    if self.main.tributes_count() == 1:
                        for c in range(0, 24):
                            if self.main.tributes[c].vigour > 0:
                                winner = c+1
                                break
                        if winner % 2 != 0:
                            dist = int((winner+1)/2)
                        else:
                            dist = int((winner)/2)
                        
                        r = []
                        if winner % 2 != 0:
                            r.append(winner-1)
                            r.append(winner)
                        else:
                            r.append(winner)
                            r.append(winner+1)
                        r.append(dist)
                        bt_next = gui.Button(self.main.frame, text='Next', command=lambda:self.main.ws.exec(r))
                    else:
                        tbs = []
                        for c in range(0, 24):
                            if self.main.tributes[c].vigour > 0:
                                tbs.append(c)
                        if tbs[1] == tbs[0] + 1:
                            dist = int((tbs[1]+1)/2)
                            r = (tbs[0], tbs[1], dist)
                            bt_next = gui.Button(self.main.frame, text='Next', command=lambda:self.main.ws.exec(r))
                        else:
                            if self.tb_ac < 23:
                                bt_next = gui.Button(self.main.frame, text='Next', command=tributes_actions)
                            else:
                                bt_next = gui.Button(self.main.frame, text='Next', command=self.main.ts.exec)
                elif self.main.tributes_count() == 0:
                    bt_next = gui.Button(self.main.frame, text='Next', command=lambda:self.main.ws.exec(-1))
                else:
                    if self.tb_ac < 23:
                        bt_next = gui.Button(self.main.frame, text='Next', command=tributes_actions)
                    else:
                        bt_next = gui.Button(self.main.frame, text='Next', command=self.main.ts.exec)
                bt_next.place(x = 400, y = 550, anchor = 'center', width=100, height=50)

                if stuff['format'] == '1':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 400, y = 300, anchor = 'center')

                if stuff['format'] == '2':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes']].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')

                if stuff['format'] == '3':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 150, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][0]].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 400, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][1]].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 650, y = 300, anchor = 'center')

                if stuff['format'] == '2x2':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 400, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][2]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 400, anchor = 'center')

                if stuff['format'] == '2x1':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 400, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][1]].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')
                
                if stuff['format'] == '1x2':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 400, anchor = 'center')
                
                if stuff['format'] == '3x1':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 450, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][2]].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')
                
                if stuff['format'] == '1x3':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_200px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][2]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 450, anchor = 'center')

                if stuff['format'] == '3x2':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 450, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][2]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][3]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 400, anchor = 'center')

                if stuff['format'] == '2x3':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 200, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 400, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][2]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][3]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 450, anchor = 'center')

                if stuff['format'] == '3x3':
                    img = gui.PhotoImage(file=self.main.tributes[self.tb_ac].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][0]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][1]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 200, y = 450, anchor = 'center')

                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][2]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 150, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][3]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 300, anchor = 'center')
                    img = gui.PhotoImage(file=self.main.tributes[stuff['extra_tributes'][4]].img_100px)
                    img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
                    img_label.photo = img
                    img_label.place(x = 600, y = 450, anchor = 'center')

        self.main.reset_window()
        self.tb_ac = -1

        title = gui.Label(self.main.frame, text = f'{self.main.time} {self.main.day}:', foreground='#000', font=('Algerian', 48), background=self.main.bg_cl)
        title.pack()

        if event == None:
            if self.main.day == 1 and self.main.time == 'Dia':
                event = 'O banho de sangue'
#            elif self.main.day % 3 == 0 and self.main.time == 'Dia':
#                event = 'Feast'
#            elif (self.main.day -1) % 3 != 0 and (self.main.day+1) % 3 == 0:
#                if choice((True, False)):
#                    event = 'event' #ph
#                else:
#                    event = ''
            else:
                event = ''

        if event != '':
            subtitile = gui.Label(self.main.frame, text = event, foreground='#000', font=('Arial Black', 22), background=self.main.bg_cl)
            subtitile.pack()
        
        if event == '' and self.main.time == 'Dia':
            text = 'O dia amanhece normalmente'
        elif event == '':
            text = 'O sol se pôs e a noite se iniciou'
        elif event == 'O banho de sangue':
            text = 'Os tributos sobem em seus pódios e a buzina soa'
        else:
            text = ''

        text_label = gui.Label(self.main.frame, text=text, foreground='#000', font=('Book Antiqua', 14), background=self.main.bg_cl)
        text_label.place(x = 400, y = 300, anchor='center')

        bt_next = gui.Button(self.main.frame, text='Next', command=tributes_actions)
        bt_next.place(x = 400, y = 550, anchor = 'center', width=100, height=50)


class win_screen:

    def __init__(self, main):
        self.main = main

    def exec(self, winner):

        self.main.reset_window()
        self.main.menu.destroy()

        if winner == -1:
            title = gui.Label(self.main.frame, text='O Hunger Games terminou em empate!', font=('Algerian', 22), foreground= '#000', background=self.main.bg_cl)
            title.pack()

            bt_close = gui.Button(self.main.frame, text='Close', command=self.main.__init__)
            bt_close.place(x = 400, y = 550, anchor = 'center', width = 100, height = 50)

        else:
            if self.main.game_mode != 'districts':
                title = gui.Label(self.main.frame, text=f'{self.main.tributes[winner].name}\né o(a) vencedor(a) do Hunger Games!', font=('Algerian', 22), foreground= '#000', background=self.main.bg_cl)
                title.pack()

                img = gui.PhotoImage(file=self.main.tributes[winner].img_200px)
                img_label = gui.Label(self.main.frame, image=img, border=False, borderwidth=0, background=self.main.bg_cl)
                img_label.photo = img
                img_label.place(x = 400, y = 300, anchor = 'center')

                bt_close = gui.Button(self.main.frame, text='Close', command=self.main.__init__)
                bt_close.place(x = 400, y = 550, anchor = 'center', width = 100, height = 50)
            else:
                title = gui.Label(self.main.frame, text=f'O distrito {winner[2]} é o vencedor do Hunger Games!', font=('Algerian', 22), foreground= '#000', background=self.main.bg_cl)
                title.pack()

                img = gui.PhotoImage(file=self.main.tributes[winner[0]].img_200px)
                img_label = gui.Label(self.main.frame, image=img, border=False, borderwidth=0, background=self.main.bg_cl)
                img_label.photo = img
                img_label.place(x = 200, y = 300, anchor = 'center')

                img = gui.PhotoImage(file=self.main.tributes[winner[1]].img_200px)
                img_label = gui.Label(self.main.frame, image=img, border=False, borderwidth=0, background=self.main.bg_cl)
                img_label.photo = img
                img_label.place(x = 600, y = 300, anchor = 'center')

                bt_close = gui.Button(self.main.frame, text='Close', command=self.main.__init__)
                bt_close.place(x = 400, y = 550, anchor = 'center', width = 100, height = 50)


class transition_screen:

    def __init__(self, main):
        self.main = main

    def exec(self):

        self.main.reset_window()

        if self.main.round_deaths > 0:      
            if self.main.time == 'Dia': l = 'o' 
            else: l = 'a'
            d = self.main.time.lower()
            title = gui.Label(self.main.frame, text= f'Fim d{l} {d} {self.main.day}:', font=('Algerian', 48), background=self.main.bg_cl)
            title.pack()

            if self.main.round_deaths > 1:
                text = gui.Label(self.main.frame, text=f'{self.main.round_deaths} disparos de canhão podem ser ouvidos à distância', font=('Book Antiqua', 12), background=self.main.bg_cl)
            else:
                text = gui.Label(self.main.frame, text=f'{self.main.round_deaths} disparo de canhão pode ser ouvido à distância', font=('Book Antiqua', 12), background=self.main.bg_cl)
            text.place(x=400, y=300, anchor='center')

            bt_next = gui.Button(self.main.frame, text= 'Next', command= lambda: self.main.st.exec(self.main.game_mode))
            bt_next.place(x=400, y=600, anchor='s', width=100, height=50)

            self.main.day_update()

        else:
            self.main.day_update()
            self.main.st.exec(self.main.game_mode)

