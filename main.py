from tribute_class import tribute
import funcs
import tkinter as gui

app = gui.Tk()
app.title('Hanger Games GUI')
app.geometry('800x600')

world_map = funcs.world_map()

app.mainloop()