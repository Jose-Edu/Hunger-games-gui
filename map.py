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

app.mainloop()