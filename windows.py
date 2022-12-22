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

        funcs.tributes_create(game_mode, self.main.tributes)
        self.main.reset_window()

        my_canvas = gui.Canvas(self.main.frame)
        my_canvas.pack(side='left', fill='both', expand='yes')

        scroll = gui_ttk.Scrollbar(self.main.frame, orient='vertical', command=my_canvas.yview)
        scroll.pack(side='right', fill='y')
        
        my_canvas.configure(yscrollcommand=scroll.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox('all')))
        def _on_mouse_wheel(event):
            my_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
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
                    gui.Label(frame, text=self.main.tributes[c+i].name, font=('Arial Black', 10), background=self.main.bg_cl, foreground='#228c22').place(x=52+i*200,y=250+c/4*190, width=100)
                else:
                    gui.Label(frame, text=self.main.tributes[c+i].name, font=('Arial Black', 10), background=self.main.bg_cl, foreground='#000').place(x=52+i*200,y=250+c/4*190, width=100)
