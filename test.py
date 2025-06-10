from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

schools = []
teachers = []
students = []

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

    def get_coordinates(self):
        import requests

        query = f"{self.name}, Siedlce, Polska"
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": query,
            "format": "json"
        }

        response = requests.get(url, params=params, headers={"User-Agent": "szkola-projekt"})
        data = response.json()

        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return [lat, lon]
        else:
            print(f"❗ Nie znaleziono współrzędnych dla: {query}")
            return [52.1676, 22.2900]  # awaryjna pozycja

        response = requests.get(url, params=params, headers={"User-Agent": "szkola-projekt"})
        data = response.json()

class Teacher:
    def __init__(self, name, surname, address, school):
        self.name = name
        self.surname = surname
        self.address = address
        self.school = school
        self.coordinates = self.get_coordinates()


class Student:
    def __init__(self, name, surname, address, school, class_name):
        self.name = name
        self.surname = surname
        self.address = address
        self.school = school
        self.class_name = class_name
        self.coordinates = self.get_coordinates()


# --- FUNKCJE ---

def add_school():
    name = entry_name.get()
    location = f"{name} w Siedlcach"
    new_school = School(name=name, location=location, map_widget=map_widget)
    schools.append(new_school)
    listbox_schools.insert(END, f"{len(schools)}. {new_school.name} ({new_school.location})")
    entry_name.delete(0, END)

def show_school_details():
    idx = listbox_schools.index(ACTIVE)
    school = schools[idx]
    map_widget.set_position(school.coordinates[0], school.coordinates[1])
    map_widget.set_zoom(16)

def delete_school():
    idx = listbox_schools.index(ACTIVE)
    schools[idx].marker.delete()
    schools.pop(idx)
    listbox_schools.delete(idx)

def delete_student():
    idx = listbox_students.index(ACTIVE)
    students.pop(idx)
    listbox_students.delete(idx)

def delete_teacher():
    idx = listbox_teachers.index(ACTIVE)
    teachers.pop(idx)
    listbox_teachers.delete(idx)

def add_example_teacher():
    if schools:
        teacher = Teacher("Anna", "Nowak", "Siedlce", schools[0])
        teachers.append(teacher)
        listbox_teachers.insert(END, f"{teacher.name} {teacher.surname} ({teacher.school.name})")
        map_widget.set_marker(teacher.coordinates[0], teacher.coordinates[1], text=teacher.name)

def add_example_student():
    if schools:
        student = Student("Jan", "Kowalski", "Siedlce", schools[0], "1A")
        students.append(student)
        listbox_students.insert(END, f"{student.name} {student.surname} ({student.class_name})")
        map_widget.set_marker(student.coordinates[0], student.coordinates[1], text=student.name)


# --- GUI ---
root = Tk()
root.title("System szkół")
root.geometry("1200x800")

frame_form = Frame(root)
frame_form.grid(row=0, column=0, padx=10, pady=10, sticky=N)

frame_lists = Frame(root)
frame_lists.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

frame_map = Frame(root)
frame_map.grid(row=1, column=0, columnspan=4)

# FORMULARZ
Label(frame_form, text="Dodaj szkołę:").grid(row=0, column=0, columnspan=2)
Label(frame_form, text="Nazwa szkoły:").grid(row=1, column=0, sticky=W)
entry_name = Entry(frame_form)
entry_name.grid(row=1, column=1)
Button(frame_form, text="Dodaj szkołę", command=add_school).grid(row=3, column=0, columnspan=2, pady=5)

# LISTA SZKÓŁ
Label(frame_lists, text="Lista szkół:").grid(row=0, column=0)
listbox_schools = Listbox(frame_lists, width=40)
listbox_schools.grid(row=1, column=0)
Button(frame_lists, text="Usuń szkołę", command=delete_school).grid(row=2, column=0, pady=2)

# LISTA UCZNIÓW
Label(frame_lists, text="Lista uczniów:").grid(row=0, column=1)
listbox_students = Listbox(frame_lists, width=40)
listbox_students.grid(row=1, column=1)
Button(frame_lists, text="Dodaj ucznia", command=add_example_student).grid(row=2, column=1)
Button(frame_lists, text="Usuń ucznia", command=delete_student).grid(row=3, column=1, pady=2)

# LISTA NAUCZYCIELI
Label(frame_lists, text="Lista nauczycieli:").grid(row=0, column=2)
listbox_teachers = Listbox(frame_lists, width=40)
listbox_teachers.grid(row=1, column=2)
Button(frame_lists, text="Dodaj nauczyciela", command=add_example_teacher).grid(row=2, column=2)
Button(frame_lists, text="Usuń nauczyciela", command=delete_teacher).grid(row=3, column=2, pady=2)

# MAPA
map_widget = tkintermapview.TkinterMapView(frame_map, width=1100, height=400)
map_widget.set_position(52.16, 22.29)
map_widget.set_zoom(12)
map_widget.grid(row=0, column=0)

root.mainloop()