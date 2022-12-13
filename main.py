#importar biblotecas e funções
from tribute_class import tribute
import funcs
import tkinter as gui
import os


#variaveis gerais
bg_cl = '#8B0000'

#criar janela
app = gui.Tk()
app.title('Hanger Games GUI')
app.geometry('800x600')
app.minsize(800, 600)
app.maxsize(800, 600)
app.configure(background= bg_cl)

#tela inicial
title = gui.Label(app, text = 'Hanger Games GUI', foreground='#000', font=('Algerian', 48), background=bg_cl)
title.pack()
del title

bt_solo = gui.Button(app, text='Solo')
bt_solo.place(width=100,height=50, x = 400, y = 350, anchor='center')

bt_doubles = gui.Button(app, text='Doubles')
bt_doubles.place(width=100,height=50, x = 400, y = 450, anchor='center')

bt_allies = gui.Button(app, text='Allies')
bt_allies.place(width=100,height=50, x = 400, y = 550, anchor='center')

path = os.path.dirname(__file__)
img = gui.PhotoImage(file=path+'\\images\\common\\logo.png')
img_label = gui.Label(app, image=img, background=bg_cl)
img_label.pack()

world_map = funcs.world_map()

app.mainloop()