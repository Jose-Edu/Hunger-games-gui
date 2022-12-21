import tkinter as gui
from windows import *


class window_base:

    app = gui.Tk()
    app.title('Hunger Games GUI')
    app.geometry('800x600')
    app.resizable(False, False)
    bg_cl = '#8B0000'
    frame = gui.Frame(app, background=bg_cl)
    frame.pack(fill='both', expand='yes')
    tributes = []


    def __init__(self):
        self.mm = main_menu(self)
        self.st = show_tributes(self)
        self.mm.exec()


    def reset_window(self):
        self.frame.destroy()
        self.frame = gui.Frame(self.app, background=self.bg_cl)
        self.frame.pack(fill='both', expand='yes')