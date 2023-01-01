import tkinter as gui
from windows import *
import os


class window_base:

    app = gui.Tk()
    app.title('Hunger Games GUI')
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


    def __init__(self):
        self.mm = main_menu(self)
        self.st = show_tributes(self)
        self.game = game(self)
        self.mm.exec()
        self.ws = win_screen(self)
        self.ts = transition_screen(self)

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
        t_count = 0

        for c in self.tributes:
            if c.vigour > 0:
                t_count += 1

        return t_count


    def day_update(self):
        if self.time == 'Dia':
            self.time = 'Noite'
        else:
            self.time = 'Dia'
            self.day += 1


    def open_tributes_info(self):
        path = os.path.dirname(__file__)
        exec(open(path+'\\tributes_info.py').read(), {'bg_cl': self.bg_cl, 'path': path, 'tributes': self.tributes}) 