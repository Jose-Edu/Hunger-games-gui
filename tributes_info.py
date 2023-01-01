import tkinter as gui


def show(tb=0):

    global frame
    frame.destroy()
    frame = gui.Frame(app, background=bg_cl)
    frame.place(x=0,y=0, width=300, height=250)

    img = gui.PhotoImage(file=tributes[tb].img_100px)
    img_label = gui.Label(frame, image = img, border = False, borderwidth = 0, background=bg_cl)
    img_label.photo = img
    img_label.place(x=0,y=0)

    txt_name_ = gui.Label(frame, text = 'Name:', font = ('Book Antiqua', 8), background=bg_cl)
    txt_name_.place(x=100, y=0)
    txt_name = gui.Label(frame, text = tributes[tb].name, font = ('Book Antiqua', 8), background=bg_cl)
    txt_name.place(x=135, y=0)

    txt_vigour_ = gui.Label(frame, text = 'Vigour:', font = ('Book Antiqua', 8), background=bg_cl)
    txt_vigour_.place(x=100, y=25)
    txt_vigour = gui.Label(frame, text = tributes[tb].vigour, font = ('Book Antiqua', 8), background=bg_cl)
    txt_vigour.place(x=140, y=25)

    txt_resource_ = gui.Label(frame, text = 'Resource:', font = ('Book Antiqua', 8), background=bg_cl)
    txt_resource_.place(x=100, y=50)
    txt_resource = gui.Label(frame, text = tributes[tb].resource, font = ('Book Antiqua', 8), background=bg_cl)
    txt_resource.place(x=150, y=50)

    txt_power_ = gui.Label(frame, text = 'Power:', font = ('Book Antiqua', 8), background=bg_cl)
    txt_power_.place(x=100, y=75)
    txt_power = gui.Label(frame, text = tributes[tb].power, font = ('Book Antiqua', 8), background=bg_cl)
    txt_power.place(x=136, y=75)

    txt_resistence_ = gui.Label(frame, text = 'Resistece:', font = ('Book Antiqua', 8), background=bg_cl)
    txt_resistence_.place(x=0, y=100)
    txt_resistence = gui.Label(frame, text = tributes[tb].resistence, font = ('Book Antiqua', 8), background=bg_cl)
    txt_resistence.place(x=50, y=100)

    txt_sanity_ = gui.Label(frame, text = 'Sanity:', font = ('Book Antiqua', 8), background=bg_cl)
    txt_sanity_.place(x=0, y=125)
    txt_sanity = gui.Label(frame, text = tributes[tb].sanity, font = ('Book Antiqua', 8), background=bg_cl)
    txt_sanity.place(x=36, y=125)

    txt_location_ = gui.Label(frame, text = 'Location:', font = ('Book Antiqua', 8), background=bg_cl)
    txt_location_.place(x=0, y=150)
    txt_location = gui.Label(frame, text = tributes[tb].location, font = ('Book Antiqua', 8), background=bg_cl)
    txt_location.place(x=50, y=150)

    txt_trait_ = gui.Label(frame, text = 'Trait:', font = ('Book Antiqua', 8), background=bg_cl)
    txt_trait_.place(x=0, y=175)
    txt_trait = gui.Label(frame, text = tributes[tb].trait, font = ('Book Antiqua', 8), background=bg_cl)
    txt_trait.place(x=30, y=175)

app = gui.Toplevel()
app.geometry('300x300')
app.resizable(False, False)
app.title('Tributes Info')
app.configure(background=bg_cl)
frame = gui.Frame(app, background=bg_cl)
frame.place(x=0,y=0, width=300, height=250)

bt_show = gui.Button(app, text='Show', command=lambda:show(int(sb.get())))
bt_show.place(x=300,y=300,anchor='se',height=50,width=100)

sb = gui.Spinbox(app, from_ = 0, to = 23, wrap=True, state='readonly')
sb.place(x=175, y=300, anchor='s', width=50, height=50)

show()

app.mainloop()