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


    def __init__(self):
        self.mm = main_menu(self)
        self.st = show_tributes(self)
        self.mm.exec()

        self.menu = gui.Menu(self.app)
        menu_actions = gui.Menu(self.menu, tearoff=0)
        menu_actions.add_command(label='Map', command=self.open_map)
        self.menu.add_cascade(label='Actions', menu=menu_actions)


    def reset_window(self):
        self.frame.destroy()
        self.frame = gui.Frame(self.app, background=self.bg_cl)
        self.frame.pack(fill='both', expand='yes')


    def open_map(self):
        path = os.path.dirname(__file__)
        exec(open(path+'\\map.py').read(), {'bg_cl': self.bg_cl, 'path': path})

    