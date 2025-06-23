from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

schools = []
teachers = []
students = []

# === KLASY ===

class School:
    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.name)

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.city}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [lat, lon]

class Teacher:
    def __init__(self, name, surname, city, school):
        self.name = name
        self.surname = surname
        self.city = city
        self.school = school
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{self.name} {self.surname}")

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.city}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [lat, lon]

class Student:
    def __init__(self, name, surname, city, school, class_name):
        self.name = name
        self.surname = surname
        self.city = city
        self.school = school
        self.class_name = class_name
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=f"{self.name} {self.surname}")

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.city}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        lon = float(soup.select(".longitude")[1].text.replace(",", "."))
        lat = float(soup.select(".latitude")[1].text.replace(",", "."))
        return [lat, lon]

# === FUNKCJE SZKÓŁ ===

def add_school():
    name = entry_school_name.get()
    city = entry_school_city.get()
    s = School(name, city)
    schools.append(s)
    entry_school_name.delete(0, END)
    entry_school_city.delete(0, END)
    entry_school_name.focus()
    update_teacher_school_menu()
    update_student_school_menu()
    show_schools()

def show_schools():
    listbox_schools.delete(0, END)
    for idx, s in enumerate(schools):
        listbox_schools.insert(idx, f"{idx+1}. {s.name} ({s.city})")

def show_school_details():
    idx = listbox_schools.index(ACTIVE)
    s = schools[idx]
    listbox_teachers_in_school.delete(0, END)
    listbox_students_in_school.delete(0, END)
    label_school_name_val.config(text=s.name)
    label_school_city_val.config(text=s.city)
    map_widget.set_position(s.coordinates[0], s.coordinates[1])
    map_widget.set_zoom(16)
    # Aktualizacja listy nauczycieli w tej szkole
    listbox_teachers_in_school.delete(0, END)
    for t in teachers:
        if t.school == s.name:
            listbox_teachers_in_school.insert(END, f"{t.name} {t.surname}")
    for st in students:
        if st.school == s.name:
            listbox_students_in_school.insert(END, f"{st.name} {st.surname}, klasa {st.class_name}")

def delete_school():
    idx = listbox_schools.index(ACTIVE)
    schools[idx].marker.delete()
    schools.pop(idx)
    show_schools()
    update_teacher_school_menu()
    update_student_school_menu()

def edit_school():
    idx = listbox_schools.index(ACTIVE)
    entry_school_name.insert(0, schools[idx].name)
    entry_school_city.insert(0, schools[idx].city)
    button_add_school.config(text="Zapisz", command=lambda: update_school(idx))
    update_teacher_school_menu()
    update_student_school_menu()

def update_school(idx):
    schools[idx].marker.delete()
    name = entry_school_name.get()
    city = entry_school_city.get()
    schools[idx].name = name
    schools[idx].city = city
    schools[idx].coordinates = schools[idx].get_coordinates()
    schools[idx].marker = map_widget.set_marker(schools[idx].coordinates[0], schools[idx].coordinates[1], text=name)
    button_add_school.config(text="Dodaj szkołę", command=add_school)
    entry_school_name.delete(0, END)
    entry_school_city.delete(0, END)
    show_schools()
    update_teacher_school_menu()
    update_student_school_menu()

# === FUNKCJE NAUCZYCIELI ===

def add_teacher():
    name = entry_teacher_name.get()
    surname = entry_teacher_surname.get()
    city = entry_teacher_city.get()
    school = var_teacher_school.get()
    t = Teacher(name, surname, city, school)
    teachers.append(t)
    entry_teacher_name.delete(0, END)
    entry_teacher_surname.delete(0, END)
    entry_teacher_city.delete(0, END)
    show_teachers()

def show_teachers():
    listbox_teachers.delete(0, END)
    for idx, t in enumerate(teachers):
        listbox_teachers.insert(idx, f"{idx+1}. {t.name} {t.surname} - {t.school} ({t.city})")

def show_teacher_details():
    idx = listbox_teachers.index(ACTIVE)
    t = teachers[idx]
    label_teacher_name_val.config(text=t.name)
    label_teacher_surname_val.config(text=t.surname)
    label_teacher_city_val.config(text=t.city)
    label_teacher_school_val.config(text=t.school)
    map_widget.set_position(t.coordinates[0], t.coordinates[1])
    map_widget.set_zoom(16)

def delete_teacher():
    idx = listbox_teachers.index(ACTIVE)
    teachers[idx].marker.delete()
    teachers.pop(idx)
    show_teachers()

def edit_teacher():
    idx = listbox_teachers.index(ACTIVE)
    t = teachers[idx]
    entry_teacher_name.insert(0, t.name)
    entry_teacher_surname.insert(0, t.surname)
    entry_teacher_city.insert(0, t.city)
    var_teacher_school.set(t.school)
    button_add_teacher.config(text="Zapisz", command=lambda: update_teacher(idx))

def update_teacher(idx):
    teachers[idx].marker.delete()
    name = entry_teacher_name.get()
    surname = entry_teacher_surname.get()
    city = entry_teacher_city.get()
    school = var_teacher_school.get()
    teachers[idx].name = name
    teachers[idx].surname = surname
    teachers[idx].city = city
    teachers[idx].school = school
    teachers[idx].coordinates = teachers[idx].get_coordinates()
    teachers[idx].marker = map_widget.set_marker(teachers[idx].coordinates[0], teachers[idx].coordinates[1], text=f"{name} {surname}")
    button_add_teacher.config(text="Dodaj nauczyciela", command=add_teacher)
    entry_teacher_name.delete(0, END)
    entry_teacher_surname.delete(0, END)
    entry_teacher_city.delete(0, END)
    show_teachers()

def update_teacher_school_menu():
    menu = optionmenu_teacher_school["menu"]
    menu.delete(0, "end")
    for school in schools:
        menu.add_command(label=school.name, command=lambda value=school.name: var_teacher_school.set(value))
    if schools:
        var_teacher_school.set(schools[0].name)

# FUNKCJE UCZNIA

def add_student():
    name = entry_student_name.get()
    surname = entry_student_surname.get()
    city = entry_student_city.get()
    school = var_student_school.get()
    class_name = entry_student_class.get()
    s = Student(name, surname, city, school, class_name)
    students.append(s)
    entry_student_name.delete(0, END)
    entry_student_surname.delete(0, END)
    entry_student_city.delete(0, END)
    entry_student_class.delete(0, END)
    show_students()

def show_students():
    listbox_students.delete(0, END)
    for idx, s in enumerate(students):
        listbox_students.insert(idx, f"{idx+1}. {s.name} {s.surname} - {s.school}, klasa {s.class_name} ({s.city})")

def show_student_details():
    idx = listbox_students.index(ACTIVE)
    s = students[idx]
    label_student_name_val.config(text=s.name)
    label_student_surname_val.config(text=s.surname)
    label_student_city_val.config(text=s.city)
    label_student_school_val.config(text=s.school)
    label_student_class_val.config(text=s.class_name)
    map_widget.set_position(s.coordinates[0], s.coordinates[1])
    map_widget.set_zoom(16)

def delete_student():
    idx = listbox_students.index(ACTIVE)
    students[idx].marker.delete()
    students.pop(idx)
    show_students()

def edit_student():
    idx = listbox_students.index(ACTIVE)
    s = students[idx]
    entry_student_name.insert(0, s.name)
    entry_student_surname.insert(0, s.surname)
    entry_student_city.insert(0, s.city)
    var_student_school.set(s.school)
    entry_student_class.insert(0, s.class_name)
    button_add_student.config(text="Zapisz", command=lambda: update_student(idx))

def update_student(idx):
    students[idx].marker.delete()
    name = entry_student_name.get()
    surname = entry_student_surname.get()
    city = entry_student_city.get()
    school = var_student_school.get()
    class_name = entry_student_class.get()
    students[idx].name = name
    students[idx].surname = surname
    students[idx].city = city
    students[idx].school = school
    students[idx].class_name = class_name
    students[idx].coordinates = students[idx].get_coordinates()
    students[idx].marker = map_widget.set_marker(
        students[idx].coordinates[0], students[idx].coordinates[1],
        text=f"{name} {surname}"
    )
    button_add_student.config(text="Dodaj ucznia", command=add_student)
    entry_student_name.delete(0, END)
    entry_student_surname.delete(0, END)
    entry_student_city.delete(0, END)
    entry_student_class.delete(0, END)
    show_students()

def update_student_school_menu():
    menu = optionmenu_student_school["menu"]
    menu.delete(0, "end")
    for school in schools:
        menu.add_command(label=school.name, command=lambda value=school.name: var_student_school.set(value))
    if schools:
        var_student_school.set(schools[0].name)

# MAPKI

def clear_all_markers():
    for s in schools:
        if s.marker:
            s.marker.delete()
            s.marker = None
    for t in teachers:
        if t.marker:
            t.marker.delete()
            t.marker = None
    for st in students:
        if st.marker:
            st.marker.delete()
            st.marker = None

def show_teacher_markers_for_school(school_name):
    clear_all_markers()
    for t in teachers:
        if t.school == school_name:
            t.marker = map_widget.set_marker(t.coordinates[0], t.coordinates[1], text=f"{t.name} {t.surname}")

def show_student_markers_for_school(school_name):
    clear_all_markers()
    for st in students:
        if st.school == school_name:
            st.marker = map_widget.set_marker(st.coordinates[0], st.coordinates[1], text=f"{st.name} {st.surname}")

def get_selected_school_name():
    idx = listbox_schools.index(ACTIVE)
    return schools[idx].name

def reset_school_map_view():
    clear_all_markers()
    idx = listbox_schools.index(ACTIVE)
    s = schools[idx]
    if s.marker is None:
        s.marker = map_widget.set_marker(s.coordinates[0], s.coordinates[1], text=s.name)
    show_school_details()

# === GUI ===

root = Tk()
root.title("System zarządzania szkołami i nauczycielami")
root.geometry("1024x800")

# === PRZYCISKI PRZEŁĄCZAJĄCE ===
button_frame = Frame(root)
button_frame.grid(row=0, column=0)

def show_schools_frame():
    frame_schools.tkraise()

def show_teachers_frame():
    frame_teachers.tkraise()

Button(button_frame, text="Pokaż szkoły", command=show_schools_frame).grid(row=0, column=0, padx=5, pady=5)
Button(button_frame, text="Pokaż nauczycieli", command=show_teachers_frame).grid(row=0, column=1, padx=5, pady=5)
Button(button_frame, text="Pokaż uczniów", command=lambda: frame_students.tkraise()).grid(row=0, column=2, padx=5, pady=5)


# === GŁÓWNE RAMKI — szkół i nauczycieli ===

frame_schools = Frame(root)
frame_schools.grid(row=1, column=0, sticky="nsew")
frame_teachers = Frame(root)
frame_teachers.grid(row=1, column=0, sticky="nsew")

# === SZKOŁY ===
frame_school_list = Frame(frame_schools)
frame_school_form = Frame(frame_schools)
frame_school_details = Frame(frame_schools)

Label(frame_school_details, text="Nauczyciele w tej szkole:").grid(row=1, column=0, sticky="w", padx=5)
listbox_teachers_in_school = Listbox(frame_school_details, width=50, height=5)
listbox_teachers_in_school.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

Label(frame_school_details, text="Uczniowie w tej szkole:").grid(row=1, column=1, sticky="w", padx=5)
listbox_students_in_school = Listbox(frame_school_details, width=50, height=5)
listbox_students_in_school.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

Label(frame_school_details, text="Nazwa:").grid(row=0, column=0, sticky="w", padx=5)
label_school_name_val = Label(frame_school_details, text="...")
label_school_name_val.grid(row=0, column=1, sticky="w", padx=5)

Label(frame_school_details, text="Miejscowość:").grid(row=0, column=2, sticky="w", padx=5)
label_school_city_val = Label(frame_school_details, text="...")
label_school_city_val.grid(row=0, column=3, sticky="w", padx=5)

frame_school_details.grid_columnconfigure(0, weight=1)
frame_school_details.grid_columnconfigure(1, weight=1)
frame_school_details.grid_columnconfigure(2, weight=0)
frame_school_details.grid_columnconfigure(3, weight=0)
frame_school_details.grid_rowconfigure(2, weight=1)

frame_school_list.grid(row=0, column=0, sticky="nsew")
frame_school_form.grid(row=0, column=1, sticky="nsew")
frame_school_details.grid(row=0, column=2, sticky="nsew")

Label(frame_school_list, text="Lista szkół:").grid(row=0, column=0, columnspan=3)
listbox_schools = Listbox(frame_school_list, width=50)
listbox_schools.grid(row=1, column=0, columnspan=3)
Button(frame_school_list, text="Pokaż szczegóły", command=show_school_details).grid(row=2, column=0)
Button(frame_school_list, text="Edytuj", command=edit_school).grid(row=2, column=1)
Button(frame_school_list, text="Usuń", command=delete_school).grid(row=2, column=2)

Label(frame_school_form, text="Nazwa szkoły:").grid(row=0, column=0)
entry_school_name = Entry(frame_school_form)
entry_school_name.grid(row=0, column=1)

Label(frame_school_form, text="Miejscowość:").grid(row=1, column=0)
entry_school_city = Entry(frame_school_form)
entry_school_city.grid(row=1, column=1)

button_add_school = Button(frame_school_form, text="Dodaj szkołę", command=add_school)
button_add_school.grid(row=2, column=0, columnspan=2)

frame_schools.grid_columnconfigure(0, weight=1)
frame_schools.grid_columnconfigure(1, weight=0)
frame_schools.grid_columnconfigure(2, weight=1)

# === NAUCZYCIELE ===

frame_teacher_list = Frame(frame_teachers)
frame_teacher_form = Frame(frame_teachers)
frame_teacher_details = Frame(frame_teachers)

frame_teacher_list.grid(row=0, column=0)
frame_teacher_form.grid(row=0, column=1)
frame_teacher_details.grid(row=0, column=2, sticky="nsew")

Label(frame_teacher_list, text="Lista nauczycieli:").grid(row=0, column=0, columnspan=3)
listbox_teachers = Listbox(frame_teacher_list, width=50)
listbox_teachers.grid(row=1, column=0, columnspan=3)
Button(frame_teacher_list, text="Pokaż szczegóły", command=show_teacher_details).grid(row=2, column=0)
Button(frame_teacher_list, text="Edytuj", command=edit_teacher).grid(row=2, column=1)
Button(frame_teacher_list, text="Usuń", command=delete_teacher).grid(row=2, column=2)

Label(frame_teacher_form, text="Imię:").grid(row=0, column=0)
entry_teacher_name = Entry(frame_teacher_form)
entry_teacher_name.grid(row=0, column=1)

Label(frame_teacher_form, text="Nazwisko:").grid(row=1, column=0)
entry_teacher_surname = Entry(frame_teacher_form)
entry_teacher_surname.grid(row=1, column=1)

Label(frame_teacher_form, text="Miejscowość:").grid(row=2, column=0)
entry_teacher_city = Entry(frame_teacher_form)
entry_teacher_city.grid(row=2, column=1)

Label(frame_teacher_form, text="Szkoła:").grid(row=3, column=0)
var_teacher_school = StringVar()
var_teacher_school.set("Brak szkół")
optionmenu_teacher_school = OptionMenu(frame_teacher_form, var_teacher_school, "Brak szkół")
optionmenu_teacher_school.grid(row=3, column=1)

button_add_teacher = Button(frame_teacher_form, text="Dodaj nauczyciela", command=add_teacher)
button_add_teacher.grid(row=4, column=0, columnspan=2)

Label(frame_teacher_details, text="Imię:").grid(row=0, column=0)
label_teacher_name_val = Label(frame_teacher_details, text="...")
label_teacher_name_val.grid(row=0, column=1)

Label(frame_teacher_details, text="Nazwisko:").grid(row=0, column=2)
label_teacher_surname_val = Label(frame_teacher_details, text="...")
label_teacher_surname_val.grid(row=0, column=3)

Label(frame_teacher_details, text="Miejscowość:").grid(row=0, column=4)
label_teacher_city_val = Label(frame_teacher_details, text="...")
label_teacher_city_val.grid(row=0, column=5)

Label(frame_teacher_details, text="Szkoła:").grid(row=0, column=6)
label_teacher_school_val = Label(frame_teacher_details, text="...")
label_teacher_school_val.grid(row=0, column=7)

# UCZNIOWIE

frame_students = Frame(root)
frame_students.grid(row=1, column=0, sticky="nsew")

frame_student_list = Frame(frame_students)
frame_student_form = Frame(frame_students)
frame_student_details = Frame(frame_students)

frame_student_list.grid(row=0, column=0)
frame_student_form.grid(row=0, column=1)
frame_student_details.grid(row=1, column=0, columnspan=2)

Label(frame_student_list, text="Lista uczniów:").grid(row=0, column=0, columnspan=3)
listbox_students = Listbox(frame_student_list, width=50)
listbox_students.grid(row=1, column=0, columnspan=3)
Button(frame_student_list, text="Pokaż szczegóły", command=show_student_details).grid(row=2, column=0)
Button(frame_student_list, text="Edytuj", command=edit_student).grid(row=2, column=1)
Button(frame_student_list, text="Usuń", command=delete_student).grid(row=2, column=2)

Label(frame_student_form, text="Imię:").grid(row=0, column=0)
entry_student_name = Entry(frame_student_form)
entry_student_name.grid(row=0, column=1)

Label(frame_student_form, text="Nazwisko:").grid(row=1, column=0)
entry_student_surname = Entry(frame_student_form)
entry_student_surname.grid(row=1, column=1)

Label(frame_student_form, text="Miejscowość:").grid(row=2, column=0)
entry_student_city = Entry(frame_student_form)
entry_student_city.grid(row=2, column=1)

Label(frame_student_form, text="Szkoła:").grid(row=3, column=0)
var_student_school = StringVar()
var_student_school.set("Brak szkół")
optionmenu_student_school = OptionMenu(frame_student_form, var_student_school, "Brak szkół")
optionmenu_student_school.grid(row=3, column=1)

Label(frame_student_form, text="Klasa:").grid(row=4, column=0)
entry_student_class = Entry(frame_student_form)
entry_student_class.grid(row=4, column=1)

button_add_student = Button(frame_student_form, text="Dodaj ucznia", command=add_student)
button_add_student.grid(row=5, column=0, columnspan=2)

Label(frame_student_details, text="Imię:").grid(row=0, column=0)
label_student_name_val = Label(frame_student_details, text="...")
label_student_name_val.grid(row=0, column=1)

Label(frame_student_details, text="Nazwisko:").grid(row=0, column=2)
label_student_surname_val = Label(frame_student_details, text="...")
label_student_surname_val.grid(row=0, column=3)

Label(frame_student_details, text="Miejscowość:").grid(row=0, column=4)
label_student_city_val = Label(frame_student_details, text="...")
label_student_city_val.grid(row=0, column=5)

Label(frame_student_details, text="Szkoła:").grid(row=0, column=6)
label_student_school_val = Label(frame_student_details, text="...")
label_student_school_val.grid(row=0, column=7)

Label(frame_student_details, text="Klasa:").grid(row=0, column=8)
label_student_class_val = Label(frame_student_details, text="...")
label_student_class_val.grid(row=0, column=9)


Button(frame_school_list, text="Pokaż nauczycieli na mapie",
       command=lambda: show_teacher_markers_for_school(get_selected_school_name())
      ).grid(row=3, column=0, columnspan=3, sticky="ew", pady=(5,0))

Button(frame_school_list, text="Pokaż uczniów na mapie",
       command=lambda: show_student_markers_for_school(get_selected_school_name())
      ).grid(row=4, column=0, columnspan=3, sticky="ew", pady=(5,10))

Button(frame_school_list, text="Resetuj widok szkoły",
       command=reset_school_map_view
      ).grid(row=5, column=0, columnspan=3, sticky="ew", pady=(0,10))

# === MAPA ===

map_widget = tkintermapview.TkinterMapView(root, width=1024, height=400)
map_widget.set_position(52.2297, 21.0122)
map_widget.set_zoom(6)
map_widget.grid(row=2, column=0, columnspan=3, sticky="nsew")

# === START ===
show_schools_frame()
root.mainloop()