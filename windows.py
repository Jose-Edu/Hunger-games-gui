import tkinter as gui
from tkinter import ttk as gui_ttk
import funcs
import os


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
        bt_next = gui.Button(frame, text='Next', command=lambda: self.main.game.exec(event='O banho de sangue'), width=20)
        bt_next.pack(side='bottom')


class game:

    tb_ac = -1

    def __init__(self, main):
        self.main = main


    def exec(self, event=''):
        def tributes_actions():
            self.main.reset_window()
            self.tb_ac += 1
            #stuff = self.main.tributes[self.tb_ac].action(event, self.main.time, self.main.tributes)
            stuff = {'format': '1', 'text': 'Text', 'extra_tributes': ()}

            title = gui.Label(self.main.frame, text = f'{self.main.time} {self.main.day}:', foreground='#000', font=('Algerian', 48), background=self.main.bg_cl)
            title.pack()
            subtitile = gui.Label(self.main.frame, text = stuff['text'], foreground='#000', font=('Book Antiqua', 12), background=self.main.bg_cl)
            subtitile.pack()
            if self.tb_ac < 23:
                bt_next = gui.Button(self.main.frame, text='Next', command=tributes_actions)
            else:
                bt_next = gui.Button(self.main.frame, text='Next', command= self.main.mm.exec)
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

        if self.main.game_mode != 'districts':
            title = gui.Label(self.main.frame, text=f'{self.main.tributes[winner].name}\né o(a) vencedor(a) do Hunger Games!', font=('Algerian', 22), foreground= '#000', background=self.main.bg_cl)
            title.pack()

            img = gui.PhotoImage(file=self.main.tributes[winner].img_200px)
            img_label = gui.Label(self.main.frame, image=img, border=False, borderwidth=0)
            img_label.photo = img
            img_label.place(x = 400, y = 300, anchor = 'center')

            bt_close = gui.Button(self.main.frame, text='Close', command=self.main.mm.exec)
            bt_close.place(x = 400, y = 550, anchor = 'center', width = 100, height = 50)
        else:
            title = gui.Label(self.main.frame, text=f'O distrito {winner[2]} é o vencedor do Hunger Games!', font=('Algerian', 22), foreground= '#000', background=self.main.bg_cl)
            title.pack()

            img = gui.PhotoImage(file=self.main.tributes[winner[0]].img_200px)
            img_label = gui.Label(self.main.frame, image=img, border=False, borderwidth=0)
            img_label.photo = img
            img_label.place(x = 200, y = 300, anchor = 'center')

            img = gui.PhotoImage(file=self.main.tributes[winner[1]].img_200px)
            img_label = gui.Label(self.main.frame, image=img, border=False, borderwidth=0)
            img_label.photo = img
            img_label.place(x = 600, y = 300, anchor = 'center')

            bt_close = gui.Button(self.main.frame, text='Close', command=self.main.mm.exec)
            bt_close.place(x = 400, y = 550, anchor = 'center', width = 100, height = 50)

