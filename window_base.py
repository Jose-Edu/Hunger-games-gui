import tkinter as gui
import funcs
import os
from windows import *


class window_base:

    app = gui.Tk()
    app.title('Hanger Games GUI')
    app.geometry('800x600')
    bg_cl = '#8B0000'
    app.minsize(800, 600)
    app.maxsize(800, 600)
    frame = gui.Frame(app, borderwidth=0, background=bg_cl)
    frame.place(width=800, height=600)
    tributes = []


    def __init__(self):
        self.mm = main_menu(self)
        self.st = show_tributes(self)
        self.mm.exec()


    def reset_window(self):
        self.frame.destroy()
        self.frame = gui.Frame(self.app, borderwidth=0, background=self.bg_cl)
        self.frame.place(width=800, height=600)