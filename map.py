import tkinter as gui

app = gui.Toplevel()
app.geometry('600x600')
app.resizable(False, False)
app.title('Map from Hunger Games')
app.configure(background=bg_cl)

_path = path+'\\images\\common\\map.png'

img = gui.PhotoImage(file=_path)
img_label = gui.Label(app, image=img, background=bg_cl)
img_label.photo = img
img_label.place(x=300,y=300, anchor='center')

for c in range(0, 24):
    if tributes[c].vigour > 0:
        img = gui.PhotoImage(file=tributes[c].img_25px)
        img_label = gui.Label(app, image=img, border=False, background=None)
        img_label.photo = img
        img_label.place(x=75+tributes[c].location[0]*75,y=75+tributes[c].location[1]*75, anchor='center')

app.mainloop()