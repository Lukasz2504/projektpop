from tkinter import *


from tkintermapview import *
import tkintermapview


root = Tk()
root.title("System szkół")
root.geometry("1024x768")

# RAMKI
ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# RAMKA LISTA OBIEKTÓW
label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista szkół:")
label_lista_obiektow.grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=50)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)

# FORMULARZ
label_formularz = Label(ramka_formularz, text="Dodaj szkołę:")
label_formularz.grid(row=0, column=0, columnspan=2)

label_name = Label(ramka_formularz, text="Nazwa szkoły:")
label_name.grid(row=1, column=0, sticky=W)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1)

label_location = Label(ramka_formularz, text="Miejscowość:")
label_location.grid(row=2, column=0, sticky=W)

entry_location = Entry(ramka_formularz)
entry_location.grid(row=2, column=1)

button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj szkołę", command=add_school)
button_dodaj_obiekt.grid(row=3, column=0, columnspan=2, pady=5)


# RAMKA SZCZEGÓŁY OBIEKTU
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Szczegóły szkoły:")
label_szczegoly_obiektu.grid(row=0, column=0, sticky=W)

label_name_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Nazwa:")
label_name_szczegoly_obiektu.grid(row=1, column=0)

label_name_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_name_szczegoly_obiektu_wartosc.grid(row=1, column=1)

label_location_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Miejscowość:")
label_location_szczegoly_obiektu.grid(row=1, column=2)

label_location_szczegoly_obiektu_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_location_szczegoly_obiektu_wartosc.grid(row=1, column=3)




root.mainloop()