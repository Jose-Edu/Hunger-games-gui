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
        bt_solo = gui.Button(self.main.frame, text='Solo')
        bt_solo.place(width=100,height=50, x = 400, y = 350, anchor='center')
        bt_districts = gui.Button(self.main.frame, text='Districts')
        bt_districts.place(width=100,height=50, x = 400, y = 450, anchor='center')
        bt_classic = gui.Button(self.main.frame, text='Classic')
        bt_classic.place(width=100,height=50, x = 400, y = 550, anchor='center')
        path = os.path.dirname(__file__)
        img = gui.PhotoImage(file=path+'\\images\\common\\logo.png')
        img_label = gui.Label(self.main.frame, image=img, background=self.main.bg_cl)
        img_label.photo = img
        img_label.pack()

        self.main.world_map = funcs.world_map()