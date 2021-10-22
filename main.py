#!/usr/bin/env python3
# coding:utf-8
# Développé par Jean Dubois
# Générateur aléatoire de personnes

from tkinter import *  # Tkinter sert à faire des fenêtres
from tkinter import ttk  # Pour faire les onglets
from tkinter import messagebox  # Pour faire des boîtes de dialogues
from tkinter import filedialog  # dialogue "enregistrer" et "ouvrir"

import os  # Pour pouvoir vérifier l'existence de fichiers et le type d'OS car ce n'est pas le même fonctionnement d'un
#            OS à l'autre.
import json  # pour lire les trads

import random  # Pour pouvoir faire du pseudo-aléatoire
from random import randint  # Pour pas avoir à écrire à chaque fois 'random.randint()'

__author__ = "Jean Dubois <jd-dev@laposte.net>"
__version__ = "4.0-rc1"
LG = "lightgreen"
PG = "palegreen"
CCEEFF = '#CCEEFF'


def ask_language():
    """ Demande la langue à l'utilisateur """
    language_window = Tk()
    language_window.title("Choix de la langue / Choose language")
    language_window.geometry("500x250")
    language_window.minsize(500, 250)
    language_window.resizable(False, False)
    try:
        language_window.iconbitmap('icon.ico')
    except TclError:
        pass
    language_window.config(background=PG)

    language_frame = Frame(language_window, bg=PG)
    language_label = Label(language_frame, text="Sélectionnez votre langue : / Choose your language:",
                           font=("Tahoma", 12), background=PG)

    language_options_list = ["Français", "English"]
    language_variable = StringVar(language_window)
    language_variable.set(language_options_list[0])

    language_opt = OptionMenu(language_frame, language_variable, *language_options_list)
    language_opt.config(width=10, font=("Tahoma", 12), bg=LG, activebackground=PG)

    language_ok_button = Button(language_frame, text="OK", font=("Tahoma", 12), bg=LG,
                                activebackground=PG, command=lambda: language_window.destroy())
    language_cancel_button = Button(language_frame, text="Annuler / Cancel", font=("Tahoma", 12), bg=LG,
                                    activebackground=PG, command=lambda: quit(0))
    language_default = IntVar()
    language_default_checkbutton = Checkbutton(language_frame, text="Définir par défaut / Set by default",
                                               activebackground=PG, variable=language_default, bg=PG)

    language_label.pack()
    language_opt.pack()
    language_default_checkbutton.pack()
    language_ok_button.pack(side=LEFT)
    language_cancel_button.pack(side=RIGHT)
    language_frame.pack(expand=YES)
    language_ok_button.focus()
    language_window.mainloop()
    language_selected = language_variable.get()
    if int(language_default.get()) == 1:
        with open('data/language.txt', 'w', encoding="UTF-8") as default_language:
            default_language.write(language_selected)
    match language_selected:
        case "Français":
            return "fr"
        case "English":
            return "en"
        case _:
            return "en"


# Définir la langue si celle-ci n'est pas définie
try:
    match open("data/language.txt", encoding="UTF-8").read().replace("\n", ""):
        case "NotSet":
            language = ask_language()
        case "Français":
            language = "fr"
        case "English":
            language = "en"
        case _:
            language = "en"
except FileNotFoundError:
    with open('data/language.txt', 'w', encoding="UTF-8") as defaultLanguage:
        defaultLanguage.write("NotSet")
    language = ask_language()

if os.path.exists(f"data/languages/{language}/translations.json"):
    # Si la langue existe
    __translations_dict__ = json.load(open(f"data/languages/{language}/translations.json", encoding="UTF-8"))
elif os.path.exists("data/languages/en/translations.txt"):
    # Langue par défaut = Anglais
    __translations_dict__ = json.load(open("data/languages/en/translations.json", encoding="UTF-8"))
else:
    # Pas de traductions
    __translations_dict__ = {
        "": "There is nothing here :)"
    }
    messagebox.showerror("Errorno", "The program can't continue because there is no translation files.\n"
                                    "Le programme ne peut pas continuer car il n'y a pas de fichiers de traduction.\n"
                                    "Lo programme pòt pas continuar perçò qu'i a pas de fichièrs de revirada.")
    quit(-1)


class Person:
    """ Définit ce qu'est une personne """

    def __init__(self, age_range=None, height_range=None, weight_range=None, gender_in_class="male", profession=None,
                 character=None, created_identity=0):
        """ Initialisation de la personne"""
        if weight_range is None:
            weight_range = [60, 65]
        if height_range is None:
            height_range = [175, 175]
        if age_range is None:
            age_range = [20, 20]
        self.created_identity = created_identity

        try:
            self.age = randint(int(age_range[0]), int(age_range[1]))  # âge en années
            if not -1 < self.age <= 122:
                self.age = 20
        except ValueError:
            self.age = 20
        except IndexError:
            self.age = 20
        if len(age_range) == 1:
            try:
                self.age = int(age_range[0])
                if not -1 < self.age <= 122:
                    self.age = 20
            except ValueError:
                self.age = 20

        try:
            self.height = randint(int(height_range[0]), int(height_range[1]))  # taille en centimètres
            if not 0 < self.height < 250:
                self.height = 175
        except ValueError:
            self.height = 175
        except IndexError:
            self.height = 175
        if len(height_range) == 1:
            try:
                self.height = int(height_range[0])
                if not 0 < self.height < 250:
                    self.height = 175
            except ValueError:
                self.height = 175
        self.height_in_meters = self.height / 100  # taille en mètres

        try:
            self.weight = randint(int(weight_range[0]), int(weight_range[1]))  # taille en centimètres
            if not 0 < self.weight < 300:
                self.weight = 60
        except ValueError:
            self.weight = 60
        except IndexError:
            self.weight = 60
        if len(weight_range) == 1:
            try:
                self.weight = int(weight_range[0])
                if not 0 < self.weight < 300:
                    self.weight = 60
            except ValueError:
                self.weight = 60

        self.bmi = self.weight / (self.height_in_meters * self.height_in_meters)  # IMC (BMI = Body Mass Index)
        self.gender_in_class = gender_in_class

        # Couleur de cheveux
        if 2 < self.age < randint(49, 55):
            if randint(1, 50) == 50:
                self.hairs_color = __translations_dict__["blue"]
            elif randint(1, 50) == 49:
                self.hairs_color = __translations_dict__["green"]
            elif randint(1, 50) == 48:
                self.hairs_color = ""
            else:
                if os.path.exists(f"data/languages/{language}/HAIRS_COLORS.txt"):
                    with open(f"data/languages/{language}/HAIRS_COLORS.txt", "r+", encoding="UTF-8") as hairs_colors_f:
                        hairs_colors_list = hairs_colors_f.readlines()
                        self.hairs_color = random.choice(hairs_colors_list).replace("\n", "")
                        hairs_colors_f.close()
                else:
                    self.hairs_color = __translations_dict__["chestnut_brown"]
        elif 2 < self.age:
            if randint(1, 25) == 1:
                self.hairs_color = __translations_dict__["grey"]
            else:
                self.hairs_color = __translations_dict__["white"]
        else:
            self.hairs_color = ""

        # Couleurs des yeux
        if randint(1, 100) == 1:
            self.eyes = "vairons"
        else:
            self.eyes = "normaux"

        if self.eyes == "normaux":
            if randint(1, 10) == 1:
                self.eyes_color = [__translations_dict__["blue"]]
            elif randint(1, 50) == 2:
                self.eyes_color = [__translations_dict__["green"]]
            elif randint(1, 100) == 3:
                self.eyes_color = [__translations_dict__["emerald_green"]]
            elif randint(1, 10000) == 1:
                self.eyes_color = [__translations_dict__["burst"]]
            elif randint(1, 2) == 1:
                self.eyes_color = [__translations_dict__["black"]]
            else:
                self.eyes_color = [__translations_dict__["chestnut_brown"]]
        else:
            self.eyes_color = ["", ""]
            while self.eyes_color[0] == self.eyes_color[1]:
                if randint(1, 10) == 1:
                    self.eyes_color[0] = __translations_dict__.get("blue")
                elif randint(1, 50) == 2:
                    self.eyes_color[0] = __translations_dict__.get("green")
                elif randint(1, 100) == 3:
                    self.eyes_color[0] = __translations_dict__.get("emerald_green")
                elif randint(1, 2) == 1:
                    self.eyes_color[0] = __translations_dict__.get("black")
                else:
                    self.eyes_color[0] = __translations_dict__.get("chestnut_brown")

                if randint(1, 10) == 1:
                    self.eyes_color[1] = __translations_dict__.get("blue")
                elif randint(1, 50) == 2:
                    self.eyes_color[1] = __translations_dict__.get("green")
                elif randint(1, 100) == 3:
                    self.eyes_color[1] = __translations_dict__.get("emerald_green")
                elif randint(1, 2) == 1:
                    self.eyes_color[1] = __translations_dict__.get("black")
                else:
                    self.eyes_color[1] = __translations_dict__.get("chestnut_brown")

        # couleur de peau
        if randint(0, 1) == 0:
            self.skin_color = __translations_dict__.get("white_feminine")
        elif randint(0, 1) == 1:
            self.skin_color = __translations_dict__.get("black_feminine")
        else:
            self.skin_color = __translations_dict__.get("mestizo")

        # Nom de famille
        # Vérification de l'existence du fichier "LAST_NAMES.txt" et choix du nom
        if os.path.exists(f"data/languages/{language}/LAST_NAMES.txt"):
            last_names_list = open(f"data/languages/{language}/LAST_NAMES.txt", "r+", encoding="UTF-8").read() \
                .split("\n")
            if randint(1, 10) == 1:
                first_last_name = random.choice(last_names_list).replace("\n", "")
                second_last_name = random.choice(last_names_list).replace("\n", "")
                if not first_last_name == second_last_name:
                    self.last_name = first_last_name + "--" + second_last_name
                else:
                    self.last_name = first_last_name
            else:
                self.last_name = random.choice(last_names_list).replace("\n", "")
        else:
            self.last_name = __translations_dict__.get("SMITH")

        # caractère
        if character is None:
            # Vérification de l'existence du fichier "CHARACTERS_LIST.txt" et choix du caractère
            if os.path.exists(f"data/languages/{language}/CHARACTERS_LIST.txt"):
                characters_list = open(f"data/languages/{language}/CHARACTERS_LIST.txt", "r+", encoding="UTF-8").read()\
                    .split("\n")
                self.character = random.choice(characters_list)
            else:
                self.character = __translations_dict__.get("is_not_found")
        else:
            self.character = character

        # Prénom
        match gender_in_class:
            case "male":
                # Vérification de l'existence du fichier "MALES_FIRST_NAMES_LIST.txt" et choix du prénom
                if os.path.exists(f"data/languages/{language}/MALES_FIRST_NAMES_LIST.txt"):
                    first_names_list = open(f"data/languages/{language}/MALES_FIRST_NAMES_LIST.txt", "r+",
                                            encoding="UTF-8").read().split('\n')
                    self.first_name = random.choice(first_names_list).replace("\n", "")
                else:
                    self.first_name = __translations_dict__.get("John")
            case "female":
                # Vérification de l'existence du fichier "FEMALES_FIRST_NAMES_LIST.txt" et choix du prénom
                if os.path.exists(f"data/languages/{language}/FEMALES_FIRST_NAMES_LIST.txt"):
                    first_names_list = open(f"data/languages/{language}/FEMALES_FIRST_NAMES_LIST.txt", "r+",
                                            encoding="UTF-8").read().split('\n')
                    self.first_name = random.choice(first_names_list).replace("\n", "")
                else:
                    self.first_name = __translations_dict__.get("Olivia")
            case _:
                self.first_name = __translations_dict__.get("Cheyenne")

        while self.last_name == self.first_name.upper():  # Si le prénom est le même que le nom
            # Vérification de l'existence du fichier "LAST_NAMES.txt" et choix du nom
            if os.path.exists(f"data/languages/{language}/LAST_NAMES.txt"):
                with open(f"data/languages/{language}/LAST_NAMES.txt", "r+", encoding="UTF-8") as last_names_file:
                    last_names_list = last_names_file.readlines()
                    last_names_file.close()
                    if randint(1, 10) == 1:
                        first_last_name = random.choice(last_names_list).replace("\n", "")
                        second_last_name = random.choice(last_names_list).replace("\n", "")
                        if not first_last_name == second_last_name:
                            self.last_name = first_last_name + "--" + second_last_name
                        else:
                            self.last_name = first_last_name
                    else:
                        self.last_name = random.choice(last_names_list).replace("\n", "")
            else:
                self.last_name = __translations_dict__.get("SMITH")
        self.last_name_list = self.last_name.split("--")

        while self.first_name.upper() in self.last_name_list:
            # Vérification de l'existence du fichier "LAST_NAMES.txt" et choix du nom
            if os.path.exists(f"data/languages/{language}/LAST_NAMES.txt"):
                with open(f"data/languages/{language}/LAST_NAMES.txt", "r+", encoding="UTF-8") as last_names_file:
                    last_names_list = last_names_file.readlines()
                    last_names_file.close()
                    if randint(1, 10) == 1:
                        first_last_name = random.choice(last_names_list).replace("\n", "")
                        second_last_name = random.choice(last_names_list).replace("\n", "")
                        if not first_last_name == second_last_name:
                            self.last_name = first_last_name + "--" + second_last_name
                        else:
                            self.last_name = first_last_name
                    else:
                        self.last_name = random.choice(last_names_list).replace("\n", "")
            else:
                self.last_name = __translations_dict__.get("SMITH")
            self.last_name_list = self.last_name.split("--")

        # Interprétation de l'IMC.
        if 16.5 > self.bmi:
            self.bmi_interpretation = __translations_dict__.get("underweight_famine")
        elif 16.5 < self.bmi < 18.5:
            self.bmi_interpretation = __translations_dict__.get("underweight")
        elif 18.5 < self.bmi < 25:
            self.bmi_interpretation = __translations_dict__.get("normal_weight")
        elif 25 < self.bmi < 30:
            self.bmi_interpretation = __translations_dict__.get("overweight")
        elif 30 < self.bmi < 35:
            self.bmi_interpretation = __translations_dict__.get("obese")
        elif 35 < self.bmi < 40:
            self.bmi_interpretation = __translations_dict__.get("severe_obese")
        else:
            self.bmi_interpretation = __translations_dict__.get("morbid_obese")

        # Profession
        if profession is None:
            if not randint(1, 10000) == 1:
                if self.age > 62:
                    self.profession = __translations_dict__.get("retired")
                elif 21 < self.age < 63:
                    # Vérification de l'existence du fichier "PROFESSIONS.txt" et choix de la profession
                    if os.path.exists(f"data/languages/{language}/PROFESSIONS.txt"):
                        with open(f"data/languages/{language}/PROFESSIONS.txt", "r+", encoding="UTF-8") as profs_file:
                            professions_list = profs_file.readlines()
                            profs_file.close()
                            self.profession = random.choice(professions_list).replace("\n", "")
                    else:
                        self.profession = __translations_dict__.get("baker")
                elif 17 < self.age < 22:
                    self.profession = __translations_dict__.get("student")
                elif 5 < self.age:
                    self.profession = __translations_dict__.get("student2")
                else:
                    if randint(0, 1) == 1 and 3 < self.age:
                        self.profession = __translations_dict__.get("student2")
                    else:
                        self.profession = None
            else:
                self.profession = __translations_dict__.get("radishes_cutter")
        else:
            self.profession = profession

    def get_age(self):
        """ Renvoie l'âge de la personne """
        return self.age

    def get_height(self):
        """ Renvoie la taille de la personne en centimètres """
        return self.height

    def get_height_in_meters(self):
        """ Renvoie la taille de la personne en mètres """
        return self.height_in_meters

    def get_weight(self):
        """ Renvoie le poids de la personne """
        return self.weight

    def get_bmi(self):
        """ Renvoie l'IMC de la personne """
        return self.bmi

    def get_bmi_interpretation(self):
        """ Renvoie l'interprétation de l'IMC de la personne.
         À noter que puisque le calcul est différent et très compliqué pour les enfants, la fonction ne renvoie
         rien si la personne est un enfant. """
        if self.age > 18:
            return self.bmi_interpretation
        else:
            return ""

    def get_first_name(self):
        """ Renvoie le prénom de la personne """
        return self.first_name

    def get_last_name(self):
        """ Renvoie le nom de famille de la personne """
        return self.last_name

    def get_gender(self):
        """ Renvoie le sexe de la personne """
        return self.gender_in_class

    def get_hairs_color(self):
        """ Renvoie la couleur des cheveux de la personne """
        return self.hairs_color

    def get_eyes_color(self):
        """ Renvoie la couleur des yeux de la personne sous forme de liste"""
        return self.eyes_color

    def get_skin_color(self):
        """ Renvoie la couleur de peau de la personne """
        return self.skin_color

    def get_profession(self):
        """ Renvoie la profession """
        return self.profession

    def get_character(self):
        """ Renvoie le caractère """
        return self.character

    def get_created_identity_number(self):
        """ Renvoie le numéro de l'id crée """
        return self.created_identity


def strint(number):
    """ Renvoie str(int(number)). Sert en gros à convertir en str la partie entière d'un float """
    return str(int(number))


def about():
    # pomme de terre frite belge
    #
    #           ~~ Lolie
    messagebox.showinfo(__translations_dict__.get("about"), (
            __translations_dict__["id_randomizer_version"] + f" {__version__}.\n" +
            __translations_dict__["dev_by"] + f" {__author__}.\n" +
            __translations_dict__["tkx"] + '\n' + __translations_dict__["tkx2"]
    ))


def add_new_created_identity(number):
    """ Ajoute 1 au nombre d'identités créées """
    global number_of_created_identities

    file = open("data/number_of_created_identities.txt", "r+", encoding="UTF-8")
    number_of_created_identities = file.readlines()
    file.close()

    number_of_created_identities = number_of_created_identities[0]
    number_of_created_identities = int(number_of_created_identities) + number

    file = open("data/number_of_created_identities.txt", "w", encoding="UTF-8")
    file.write(str(number_of_created_identities))
    file.close()


def open_saved_document(name_of_element="Document"):
    """ Ouvre le document à rappeler """
    if os.path.exists(name_of_element):
        try:
            with open(name_of_element, "r", encoding="UTF-8") as file:
                person_saved = file.read().split("\n")
                file.close()
            person_name = person_saved[1].replace("\n", '') + " " + person_saved[2].replace("\n", '')
            age = person_saved[3].replace("\n", '')
            gender_in_function_open_saved_document = person_saved[4].replace("\n", '')
            skin_color = person_saved[5].replace("\n", '')
            eyes_color = person_saved[6].replace("\n", '').replace('[', '').replace(']', '') + ','
            eyes_color = eyes_color.split(',')
            del eyes_color[-1]
            hairs_color = person_saved[7].replace("\n", '')
            height_in_meters = person_saved[8].replace("\n", '')
            weight = person_saved[9].replace("\n", '')
            bmi = float(person_saved[10].replace("\n", ''))
            bmi_interpretation = person_saved[11].replace("\n", '')
            profession = person_saved[12].replace("\n", '')
            character = person_saved[13].replace("\n", '')
        except Exception as e:
            messagebox.showerror(__translations_dict__["error"], __translations_dict__.get("not_person_file") + '\n'
                                 + __translations_dict__["error_code"] + "python." + e.__class__.__name__)
            return "invalidFileError : " + e.__class__.__name__

        result_frame = Frame(tabs, bg=PG)

        result_label1 = Label(result_frame, text=(
                person_name + " " + __translations_dict__["age_is"] + " " +
                str(age) + " " + __translations_dict__["years_old"] + ","
        ), font=("Tahoma", 12), bg=PG)
        result_label1_bis = Label(result_frame, text=(__translations_dict__["have_color_skin"] % skin_color + ","),
                                  font=("Tahoma", 12), bg=PG)
        result_label1_bis2 = Label(result_frame, text=character, font=("Tahoma", 12), bg=PG)

        if profession is not None:
            result_label1_ter = Label(result_frame, text=(__translations_dict__["is"] + " " + profession + ","),
                                      font=("Tahoma", 12), bg=PG)
        else:
            result_label1_ter = None

        if len(eyes_color) == 1:
            result_label2 = Label(result_frame, text=(
                    __translations_dict__["have_color_eyes"] % eyes_color[0].replace("'", "") + ","),
                                  font=("Tahoma", 12), bg=PG)
        else:
            result_label2 = Label(result_frame, text=(
                    __translations_dict__["minnow1"] + " " + eyes_color[0].replace("'", "") + " " +
                    __translations_dict__["minnow2"] % eyes_color[1].replace("'", "") + ","),
                                  font=("Tahoma", 12), bg=PG)

        if not hairs_color == "":
            result_label3 = Label(result_frame,
                                  text=(__translations_dict__["have_color_hairs"] % hairs_color + ","),
                                  font=("Tahoma", 12), bg=PG
                                  )
        else:
            result_label3 = Label(result_frame, text=__translations_dict__["bald"], font=("Tahoma", 12), bg=PG)

        result_label4 = Label(result_frame, text=(__translations_dict__["have_(meters_tall)"] + " " +
                                                  str(height_in_meters) + " " +
                                                  __translations_dict__["(have_)meters_tall"] + ","),
                              font=("Tahoma", 12), bg=PG)
        result_label5 = Label(result_frame, text=(__translations_dict__["weigh_(kilo)"] + " " + str(weight) + " " +
                                                  __translations_dict__["kilo"] + ","),
                              font=("Tahoma", 12), bg=PG)
        result_label6 = Label(result_frame, text=(__translations_dict__["have_a_BMI_around"] + " " +
                                                  strint(bmi) + "."),
                              font=("Tahoma", 12), bg=PG)

        if not bmi_interpretation == "":
            if gender_in_function_open_saved_document == "male":
                result_label7 = Label(result_frame, text=(__translations_dict__.get("BMI_so_he_is") + " " +
                                                          bmi_interpretation + "."), font=("Tahoma", 12), bg=PG)
            else:
                result_label7 = Label(result_frame, text=(__translations_dict__.get("BMI_so_she_is") + " " +
                                                          bmi_interpretation + "."), font=("Tahoma", 12), bg=PG)
        else:
            result_label7 = Label(result_frame, text="", font=("Tahoma", 12), bg=PG)

        close_button = Button(result_frame, text=__translations_dict__.get("close"), font=("Tahoma", 12), bg=LG,
                              activebackground=CCEEFF, command=lambda: tabs.forget(result_frame))

        result_label1.pack()
        result_label1_bis.pack()
        result_label1_bis2.pack()
        if result_label1_ter is not None:
            result_label1_ter.pack()
        result_label2.pack()
        result_label3.pack()
        result_label4.pack()
        result_label5.pack()
        result_label6.pack()
        result_label7.pack()
        close_button.pack()
        filename = name_of_element.split("/")
        filename = filename[len(filename) - 1].replace(".person", '')
        tabs.add(result_frame, text=(
                __translations_dict__.get("created_id_number") +
                person_saved[0].replace("\n", '') +
                " - " + filename)
                 )
        tabs.select(result_frame)
        return
    else:
        messagebox.showerror(__translations_dict__.get("error"), __translations_dict__.get("save_does_not_exist"))
        return


def ask_for_document_saved():
    """ Demande le document à ouvrir. """

    filename = filedialog.askopenfilename(initialdir="saves/", title=__translations_dict__.get("select_person"),
                                          filetypes=(
                                              (__translations_dict__.get("person_files"), "*.person*"),
                                              (__translations_dict__.get("all_files_open"), "*.*")
                                          ))
    if filename != "":
        open_saved_document(filename)


def save(person, name="Document"):
    """ Sauvegarde """
    try:
        if name.endswith(".person"):
            filename = name
        else:
            if "." not in name:
                filename = name + ".person"
            else:
                if messagebox.askyesno(__translations_dict__.get("question"),
                                       __translations_dict__.get("file_have_not_ext") + "\n" +
                                       __translations_dict__.get("do_you_want_to_add_ext")):
                    filename = name + ".person"
                else:
                    filename = name
        file = open(filename, "w", encoding="UTF-8")
        file.write(str(person.get_created_identity_number()) + "\n")
        file.write(str(person.get_first_name()) + "\n")
        file.write(str(person.get_last_name()) + "\n")
        file.write(str(person.get_age()) + "\n")
        file.write(str(person.get_gender()) + "\n")
        file.write(str(person.get_skin_color()) + "\n")
        file.write(str(person.get_eyes_color()) + "\n")
        file.write(str(person.get_hairs_color()) + "\n")
        file.write(str(person.get_height_in_meters()) + "\n")
        file.write(str(person.get_weight()) + "\n")
        file.write(str(person.get_bmi()) + "\n")
        file.write(str(person.get_bmi_interpretation()) + "\n")
        file.write(str(person.get_profession()) + "\n")
        file.write(str(person.get_character()) + "\n")
        file.close()
        # OBTW
        #   explication du filename.split("/")[len(filename.split('/')) - 1] :
        #   filename.split("/") : on fait une liste du type ["C:", "Users", "User", "Desktop", "save.person"]
        #   [len(filename.split('/')) - 1] : on prend le dernier élément de cette liste, ici save.person
        # TLDR
        messagebox.showinfo(__translations_dict__.get("info"), (__translations_dict__.get("saved") + "\n" +
                                                                filename.split("/")[len(filename.split('/')) - 1]
                                                                )
                            )
    except OSError:
        messagebox.showerror(__translations_dict__.get("error"), __translations_dict__.get("this_name_is_not_accepted"))


def save_as(person):
    """ Demande le nom de la sauvegarde. """
    filename = filedialog.asksaveasfilename(initialdir="saves/", title=__translations_dict__.get("save_person"),
                                            filetypes=(
                                                (__translations_dict__.get("person_files"), "*.person"),
                                                (__translations_dict__.get("all_files_save"), "*.*")
                                            ))
    if filename != "":
        save(person, filename)


def reset_data():
    """ Réinitialise les données """
    global number_of_created_identities
    # demander à l'utilisateur s'il est sûr de réinitialiser les données
    are_you_sure = messagebox.askquestion(__translations_dict__.get("confirmation"),
                                          __translations_dict__.get("are_you_sure") + "\n" +
                                          __translations_dict__.get("are_you_sure2"), default='no')
    if are_you_sure == "yes":
        file = open("data/number_of_created_identities.txt", "w", encoding="UTF-8")
        file.write("0")
        file.close()
        number_of_created_identities = 0

        messagebox.showinfo(__translations_dict__.get("info"), __translations_dict__.get("data_successfully_reinit"))
        with open('data/language.txt', 'w', encoding="UTF-8") as default_language_file:
            default_language_file.write("NotSet")
            default_language_file.close()
    else:
        messagebox.showinfo(__translations_dict__.get("info"), __translations_dict__.get("data_not_reinit"))


def result(_gender, _age_range_entry, _height_range_entry, _weight_range_entry, _profession_str_var,
           _character_str_var):
    """ Créé l'onglet où la personne est indiquée """
    global number_of_created_identities
    try:
        add_new_created_identity(1)
    except FileNotFoundError:
        # Fichier manquant : terminer la fonction en affichant une erreur
        messagebox.showerror(__translations_dict__["FileNotFoundError"],
                             __translations_dict__["crash_file_missing"] + "\n\n" +
                             __translations_dict__["please_reinit_data"])
        return "FileNotFoundError"
    if _gender == "randomize":
        randomized = True
        pseudo_random_number = randint(0, 1)
        if pseudo_random_number == 0:
            _gender = "female"
        else:
            _gender = "male"
    else:
        randomized = False
    if _profession_str_var.get() == __translations_dict__["randomize"]:
        prof_randomize = True
    else:
        prof_randomize = False
    if _character_str_var.get() == __translations_dict__["randomize"]:
        char_randomize = True
    else:
        char_randomize = False
    age_range_entered = _age_range_entry.get()
    age_range_in_function = age_range_entered.split('.')
    height_range_entered = _height_range_entry.get()
    height_range_in_function = height_range_entered.split('.')
    weight_range_entered = _weight_range_entry.get()
    weight_range_in_function = weight_range_entered.split('.')

    person = Person(age_range_in_function, height_range_in_function, weight_range_in_function, _gender,
                    created_identity=number_of_created_identities,
                    profession=(_profession_str_var.get() if not prof_randomize else None),
                    character=(_character_str_var.get() if not char_randomize else None)
                    )
    person_name = person.get_first_name() + " " + person.get_last_name()
    person_age = person.get_age()
    person_character = person.get_character()
    skin_color = person.get_skin_color()
    hairs_color = person.get_hairs_color()

    result_frame = Frame(tabs, bg=PG)

    result_label1 = Label(result_frame, text=(person_name + " " + __translations_dict__["age_is"] + " " +
                                              str(person_age) + " " + __translations_dict__["years_old"] + ","),
                          font=("Tahoma", 12), bg=PG)

    result_label1_bis = Label(result_frame, text=(__translations_dict__["have_color_skin"] % str(skin_color) + ","),
                              font=("Tahoma", 12), bg=PG)
    result_label1_bis2 = Label(result_frame, text=str(person_character), font=("Tahoma", 12), bg=PG)

    if person.get_profession() is not None:
        result_label1_ter = Label(result_frame, text=(__translations_dict__["is"] + " " + str(person.get_profession())
                                                      + ","),
                                  font=("Tahoma", 12), bg=PG)
    else:
        result_label1_ter = None

    if len(person.get_eyes_color()) == 1:
        result_label2 = Label(result_frame,
                              text=(__translations_dict__["have_color_eyes"] % person.get_eyes_color()[0] + ","),
                              font=("Tahoma", 12), bg=PG)
    else:
        result_label2 = Label(result_frame,
                              text=(__translations_dict__["minnow1"] + " " + person.get_eyes_color()[0] + " " +
                                    __translations_dict__["minnow2"] % person.get_eyes_color()[1] + ","),
                              font=("Tahoma", 12), bg=PG)

    if person.get_hairs_color() != "":
        result_label3 = Label(result_frame, text=(__translations_dict__["have_color_hairs"] % hairs_color + ","),
                              font=("Tahoma", 12), bg=PG)
    else:
        result_label3 = Label(result_frame, text=__translations_dict__["bald"], font=("Tahoma", 12), bg=PG)

    result_label4 = Label(result_frame, text=(__translations_dict__["have_(meters_tall)"] + " " +
                                              str(person.get_height_in_meters()) + " " +
                                              __translations_dict__["(have_)meters_tall"] + ","),
                          font=("Tahoma", 12), bg=PG)

    result_label5 = Label(result_frame, text=(__translations_dict__["weigh_(kilo)"] + " " + str(person.get_weight())
                                              + " " + __translations_dict__["kilo"] + ","), font=("Tahoma", 12),
                          bg=PG)

    result_label6 = Label(result_frame, text=(__translations_dict__["have_a_BMI_around"] + " " +
                                              strint(person.get_bmi()) + "."),
                          font=("Tahoma", 12), bg=PG)

    if person.get_bmi_interpretation() != "":
        if _gender == "male":
            result_label7 = Label(result_frame, text=(__translations_dict__["BMI_so_he_is"] + " " +
                                                      person.get_bmi_interpretation() + "."),
                                  font=("Tahoma", 12), bg=PG)
        else:
            result_label7 = Label(result_frame, text=(__translations_dict__["BMI_so_she_is"] + " " +
                                                      person.get_bmi_interpretation() + "."),
                                  font=("Tahoma", 12), bg=PG)
    else:
        result_label7 = Label(result_frame, text="", font=("Tahoma", 12), bg=PG)
    if randomized:
        _gender = "randomize"

    save_button = Button(result_frame, text=__translations_dict__["save"], font=("Tahoma", 12), bg=LG,
                         activebackground=CCEEFF, command=lambda: save_as(person))
    close_button = Button(result_frame, text=__translations_dict__["close"], font=("Tahoma", 12), bg=LG,
                          activebackground=CCEEFF, command=lambda: tabs.forget(result_frame))

    # empaquetage
    result_label1.pack()
    result_label1_bis.pack()
    result_label1_bis2.pack()
    if result_label1_ter is not None:
        result_label1_ter.pack()
    result_label2.pack()
    result_label3.pack()
    result_label4.pack()
    result_label5.pack()
    result_label6.pack()
    result_label7.pack()
    save_button.pack()
    close_button.pack()

    tabs.add(result_frame, text=__translations_dict__["created_id_number"] + str(number_of_created_identities))
    tabs.select(result_frame)
    all_tabs = list(tabs.tabs())[1:]

    if len(all_tabs) == 200:
        messagebox.showerror("Ban", "You was banned from PersonCraft for reason : autoclick")


def change_to_male():
    """ Mets gender à "male" """
    global gender
    gender = "male"


def change_to_female():
    """ Mets gender à "female" """
    global gender
    gender = "female"


def randomize_gender():
    """ Randomise le gender """
    global gender
    gender = "randomize"


def close_all_tabs():
    """ Ferme tous les onglets """
    global tabs
    all_tabs = list(tabs.tabs())[1:]  # on enlève l'accueil

    for tab in all_tabs:
        tabs.forget(tab)


number_of_created_identities = 0

# Création de la fenêtre
root = Tk()
root.title(__translations_dict__["win_title"])
# ligne suivante : j'utilise cette trad pour vérifier que les caractères sont correctement décodés.
# Dé-commenter en cas de besoin.
# print(__translations_dict__["win_title"])
root.geometry("990x600")
root.minsize(900, 500)

# Sous Linux, tkinter plante avec TclError lorsqu'on charge l'icône.
try:
    root.iconbitmap('icon.ico')
except TclError:
    pass
root.config(background=PG)

tabs = ttk.Notebook(root)

# Création d'une frame
frame1 = Frame(tabs, bg=PG)

tabs.add(frame1, text=__translations_dict__["home"])
tabs.pack(expand=1, fill="both")

# Création du titre et de texte
title_label = Label(frame1, text=__translations_dict__["win_title"], font=('Tahoma', 40), bg=PG)
label1 = Label(frame1, text=" ", font=('Tahoma', 15), bg=PG)

# Sexe
gender_label = Label(frame1, text=__translations_dict__["gender"], font=('Tahoma', 15), bg=PG)
gender = "randomize"
gender_radiobuttons = IntVar()
gender_randomize_radio = Radiobutton(frame1, text=__translations_dict__["randomize"], variable=gender_radiobuttons,
                                     bg=PG, activebackground=PG, value=0, command=lambda: randomize_gender())
gender_female_radio = Radiobutton(frame1, text=__translations_dict__["female"], variable=gender_radiobuttons, bg=PG,
                                  activebackground=PG, value=1, command=lambda: change_to_female())
gender_male_radio = Radiobutton(frame1, text=__translations_dict__["male"], variable=gender_radiobuttons, bg=PG,
                                activebackground=PG, value=2, command=lambda: change_to_male())

# Profession
profession_label = Label(frame1, text=__translations_dict__["profession"], font=('Tahoma', 15), bg=PG)
professions = [__translations_dict__["randomize"]] + [
    prof.replace("\n", '') for prof in open(f"data/languages/{language}/PROFESSIONS.txt", 'r+', encoding='UTF-8')
        .readlines()
]
profession_str_var = StringVar(frame1)
profession_str_var.set(professions[0])
profession_opt = OptionMenu(frame1, profession_str_var, *professions)
profession_opt.config(width=30, font=("Tahoma", 12), bg=LG, activebackground=PG)

# Caractères
character_label = Label(frame1, text=__translations_dict__["character"], font=('Tahoma', 15), bg=PG)
characters = [__translations_dict__["randomize"]] + [
    prof.replace("\n", '') for prof in open(f"data/languages/{language}/CHARACTERS_LIST.txt", 'r+', encoding='UTF-8')
        .readlines()
]
character_str_var = StringVar(frame1)
character_str_var.set(characters[0])
character_opt = OptionMenu(frame1, character_str_var, *characters)
character_opt.config(width=30, font=("Tahoma", 12), bg=LG, activebackground=PG)

# Tranche d'âge
age_label = Label(frame1, text=__translations_dict__["age_range"] + __translations_dict__["separate_by_dot"],
                  font=('Tahoma', 15), bg=PG)
age_range_entry = Entry(frame1, bg=LG)

# Tranche de taille
height_label = Label(frame1, text=__translations_dict__["height_range"] + __translations_dict__["separate_by_dot"],
                     font=('Tahoma', 15), bg=PG)
height_range_entry = Entry(frame1, bg=LG)

# Tranche de poids
weight_label = Label(frame1, text=__translations_dict__["weight_range"] + __translations_dict__["separate_by_dot"],
                     font=('Tahoma', 15), bg=PG)
weight_range_entry = Entry(frame1, bg=LG)

# Bouton OK
label2 = Label(frame1, text=" ", font=('Tahoma', 10), bg=PG)
OK_button = Button(frame1, text=__translations_dict__["submit"], font=("Tahoma", 10), bg=LG,
                   activebackground=CCEEFF, command=lambda: result(_gender=gender,
                                                                   _age_range_entry=age_range_entry,
                                                                   _height_range_entry=height_range_entry,
                                                                   _weight_range_entry=weight_range_entry,
                                                                   _profession_str_var=profession_str_var,
                                                                   _character_str_var=character_str_var)
                   )

# Ajout d'un menu
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
# réinitialiser données
file_menu.add_command(label=__translations_dict__["reinit_data"], command=lambda: reset_data(), accelerator="Ctrl+R")
# ouvrir...
file_menu.add_command(label=__translations_dict__["open..."], command=lambda: ask_for_document_saved(),
                      accelerator="Ctrl+O")
menu_bar.add_cascade(label=__translations_dict__["file"], menu=file_menu)
options_menu = Menu(menu_bar, tearoff=0)
# Bouton OK
options_menu.add_command(label=__translations_dict__["submit"], command=lambda: result(
    _gender=gender,
    _age_range_entry=age_range_entry,
    _height_range_entry=height_range_entry,
    _weight_range_entry=weight_range_entry,
    _profession_str_var=profession_str_var,
    _character_str_var=character_str_var), accelerator=__translations_dict__["enter"])
# fermer tous les onglets
options_menu.add_command(label=__translations_dict__["close_all_tabs"], command=lambda: close_all_tabs(),
                         accelerator="Ctrl+F1")
options_menu.add_separator()
# à propos du programme
options_menu.add_command(label=__translations_dict__["about..."], command=lambda: about(),
                         accelerator=f"Ctrl+{__translations_dict__['shift']}+A")
# quitter le programme
options_menu.add_command(label=__translations_dict__["quit"], command=lambda: quit(0), accelerator="Ctrl+Q")
menu_bar.add_cascade(label=__translations_dict__["options"], menu=options_menu)
root.config(menu=menu_bar)

# Empaquetage
title_label.pack()
label1.pack()
gender_label.pack()
gender_randomize_radio.pack()
gender_female_radio.pack()
gender_male_radio.pack()
profession_label.pack()
profession_opt.pack()
character_label.pack()
character_opt.pack()
age_label.pack()
age_range_entry.pack()
height_label.pack()
height_range_entry.pack()
weight_label.pack()
weight_range_entry.pack()
label2.pack()
OK_button.pack()

# raccourcis clavier
root.bind('<Control-q>', lambda event: exit())
root.bind('<Control-r>', lambda event: reset_data())
root.bind('<Control-o>', lambda event: ask_for_document_saved())
root.bind('<Control-F1>', lambda event: close_all_tabs())
root.bind('<Control-Shift-A>', lambda event: about())
root.bind('<Return>',
          lambda event, g=gender, a=age_range_entry, h=height_range_entry,
          w=weight_range_entry, p=profession_str_var, c=character_str_var: result(g, a, h, w, p, c)
          )
root.mainloop()
quit(0)

# Merci d'utiliser mon programme :)
