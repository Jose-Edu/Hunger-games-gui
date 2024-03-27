import tkinter as gui
from windows import *
import os
import funcs


class window_base:

    app = gui.Tk()
    app.title('Hunger Games GUI')
    app.iconbitmap('images//common//ico.ico')
    app.geometry('800x600')
    app.resizable(False, False)
    bg_cl = '#8B0000'
    frame = gui.Frame(app, background=bg_cl)
    frame.pack(fill='both', expand='yes')
    tributes = []
    menu = gui.Menu(app)
    day = 1
    time = 'Dia'
    game_mode = ''
    round_deaths = 0
    world_map = funcs.world_map()


    def __init__(self):
        self.mm = main_menu(self)
        self.st = show_tributes(self)
        self.game = game(self)
        self.mm.exec()
        self.ws = win_screen(self)
        self.ts = transition_screen(self)

        self.tributes = []
        self.menu = gui.Menu(self.app)
        self.day = 1
        self.time = 'Dia'
        self.game_mode = ''
        self.round_deaths = 0

        self.menu = gui.Menu(self.app)
        menu_actions = gui.Menu(self.menu, tearoff=0)
        menu_actions.add_command(label='Map', command=self.open_map)
        menu_actions.add_command(label='Tributes Info', command=self.open_tributes_info)
        self.menu.add_cascade(label='Actions', menu=menu_actions)


    def reset_window(self):
        self.frame.destroy()
        self.frame = gui.Frame(self.app, background=self.bg_cl)
        self.frame.pack(fill='both', expand='yes')


    def open_map(self):
        path = os.path.dirname(__file__)
        exec(open(path+'\\map.py').read(), {'bg_cl': self.bg_cl, 'path': path, 'tributes': self.tributes})


    def tributes_count(self):
        t_count = 24

        for c in self.tributes:
            if c.vigour < 1:
                t_count -= 1

        return t_count


    def day_update(self):
        if self.time == 'Dia':
            self.time = 'Noite'
        else:
            self.time = 'Dia'
            self.day += 1
        self.round_deaths = 0
        for t in self.tributes:
            t.update(self.tributes)


    def open_tributes_info(self):
        path = os.path.dirname(__file__)
        exec(open(path+'\\tributes_info.py').read(), {'bg_cl': self.bg_cl, 'path': path, 'tributes': self.tributes}) 


_global_ = window_base()

_global_.app.mainloop()