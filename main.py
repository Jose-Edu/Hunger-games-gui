#importar biblotecas e funções
import funcs
import tkinter as gui
import os


#variaveis gerais
bg_cl = '#8B0000'

#criar janela e frame
app = gui.Tk()
app.title('Hanger Games GUI')
app.geometry('800x600')
app.minsize(800, 600)
app.maxsize(800, 600)
frame = gui.Frame(app, borderwidth=0, background=bg_cl)
frame.place(width=800, height=600)

#tela inicial
title = gui.Label(frame, text = 'Hanger Games GUI', foreground='#000', font=('Algerian', 48), background=bg_cl)
title.pack()
bt_solo = gui.Button(frame, text='Solo')
bt_solo.place(width=100,height=50, x = 400, y = 350, anchor='center')
bt_districts = gui.Button(frame, text='Districts')
bt_districts.place(width=100,height=50, x = 400, y = 450, anchor='center')
bt_classic = gui.Button(frame, text='Classic')
bt_classic.place(width=100,height=50, x = 400, y = 550, anchor='center')
path = os.path.dirname(__file__)
img = gui.PhotoImage(file=path+'\\images\\common\\logo.png')
img_label = gui.Label(frame, image=img, background=bg_cl)
img_label.pack()

world_map = funcs.world_map()

app.mainloop()