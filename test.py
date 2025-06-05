from tkinter import *
import tkintermapview


schools:list = []

class School:
    def __init__(self, name, location, map_widget):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(
            self.coordinates[0],
            self.coordinates[1],
            text=self.name
        )

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup

        address_url: str = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(address_url).text
        response_html = BeautifulSoup(response, "html.parser")

        longitude: float = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude: float = float(response_html.select(".latitude")[1].text.replace(",", "."))
        return [latitude, longitude]

def add_school():
    name = entry_name.get()
    location = entry_location.get()
    new_school = School(name=name, location=location, map_widget=map_widget)
    schools.append(new_school)
    listbox_lista_obiektow.insert(END, f"{len(schools)}. {new_school.name} ({new_school.location})")
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_name.focus()

    print(f"Dodano szkołę: {new_school.name}, {new_school.location}")

def delete_school():
    idx = listbox_lista_obiektow.index(ACTIVE)
    schools[idx].marker.delete()
    schools.pop(idx)
    listbox_lista_obiektow.delete(idx)
    label_name_szczegoly_obiektu_wartosc.config(text="....")
    label_location_szczegoly_obiektu_wartosc.config(text="....")


def show_school_details():
    idx = listbox_lista_obiektow.index(ACTIVE)
    school = schools[idx]
    label_name_szczegoly_obiektu_wartosc.config(text=school.name)
    label_location_szczegoly_obiektu_wartosc.config(text=school.location)
    map_widget.set_position(school.coordinates[0], school.coordinates[1])
    map_widget.set_zoom(16)

def edit_school():
    idx = listbox_lista_obiektow.index(ACTIVE)
    school = schools[idx]
    entry_name.delete(0, END)
    entry_name.insert(0, school.name)

    entry_location.delete(0, END)
    entry_location.insert(0, school.location)

    button_dodaj_obiekt.config(text="Zapisz",command=lambda: update_school(idx))


def update_school(idx):
    name = entry_name.get()
    location = entry_location.get()

    schools[idx].marker.delete()

    schools[idx].name = name
    schools[idx].location = location
    schools[idx].coordinates = schools[idx].get_coordinates()
    schools[idx].marker = map_widget.set_marker(
        schools[idx].coordinates[0],
        schools[idx].coordinates[1],
        text=schools[idx].name
    )

    button_dodaj_obiekt.config(text="Dodaj szkołę", command=add_school)
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_name.focus()

    listbox_lista_obiektow.delete(idx)
    listbox_lista_obiektow.insert(idx, f"{idx+1}. {name} ({location})")



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

button_pokaz_szczegoly = Button(ramka_lista_obiektow, text="Pokaż szczegóły", command=show_school_details)
button_pokaz_szczegoly.grid(row=2, column=0, columnspan=3)
button_edytuj = Button(ramka_lista_obiektow, text="Edytuj szkołę", command=edit_school)
button_edytuj.grid(row=3, column=0, columnspan=3)
button_usun = Button(ramka_lista_obiektow, text="Usuń szkołę", command=delete_school)
button_usun.grid(row=4, column=0, columnspan=3)
button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj szkołę", command=add_school)
button_dodaj_obiekt.grid(row=3, column=0, columnspan=2)

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

map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1024, height=400)
map_widget.set_position(52.16, 22.29)  # Siedlce
map_widget.set_zoom(12)
map_widget.grid(row=0, column=0, columnspan=8)




root.mainloop()