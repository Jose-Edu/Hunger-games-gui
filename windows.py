import tkinter as gui
import funcs
import os


class main_menu:

    def __init__(self, main):
        self.main = main


    def exec(self):
        self.main.reset_window()
        
        title = gui.Label(self.main.frame, text = 'Hanger Games GUI', foreground='#000', font=('Algerian', 48), background=self.main.bg_cl)
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
        sb = gui.Scrollbar(self.main.frame, orient='vertical')
        sb.pack(side='right', fill='y')
        title = gui.Label(self.main.frame, text = 'Tributos', foreground='#000', font=('Algerian', 48), background=self.main.bg_cl)
        title.pack()
        gui.Label(self.main.frame, image=gui.PhotoImage(file=self.main.tributes[1].img_100px)).pack()

