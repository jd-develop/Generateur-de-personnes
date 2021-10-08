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
import shutil  # Pour traficoter les fichiers

import random  # Pour pouvoir faire du pseudo-aléatoire
from random import randint  # Pour pas avoir à écrire à chaque fois 'random.randint()'


__author__ = "Jean Dubois <jd-dev@laposte.net>"
__version__ = "3.0.1"


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
    language_window.config(background='palegreen')

    language_frame = Frame(language_window, bg="palegreen")
    language_label = Label(language_frame, text="Sélectionnez votre langue : / Choose your language :", font=("Tahoma",
                                                                                                              12),
                           background="palegreen")
    
    language_options_list = ["Français", "English"]
    language_variable = StringVar(language_window)
    language_variable.set(language_options_list[0])

    language_opt = OptionMenu(language_frame, language_variable, *language_options_list)
    language_opt.config(width=10, font=("Tahoma", 12), bg="lightgreen", activebackground='palegreen')

    language_ok_button = Button(language_frame, text="OK", font=("Tahoma", 12), bg="lightgreen",
                                activebackground='palegreen', command=lambda: language_window.destroy())
    language_cancel_button = Button(language_frame, text="Annuler", font=("Tahoma", 12), bg="lightgreen",
                                    activebackground='palegreen', command=lambda: quit(0))
    language_default = IntVar()
    language_default_checkbutton = Checkbutton(language_frame, text="Définir par défaut / Set by default",
                                               activebackground='palegreen', variable=language_default, bg="palegreen")
    
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
        with open('data/language.txt', 'w') as default_language:
            default_language.write(language_selected)
    match language_selected:
        case "Français":
            return "fr"
        case "English":
            return "en"
        case _:
            return "en"


def decode_text_document(str_doc, antislash_n=False):
    """ Décode les documents texte non-UTF-8 """
    if not antislash_n:
        return str_doc.replace("Ã©", "é").replace("Ã¢", "â").replace("Ã¨", "è").replace("Ã‰", "É").replace("Â°", "°")\
            .replace("Ã€", "À").replace("ÃŠ", "Ê").replace("Ã»", "û").replace("Ã ", "à").replace("Ã¯", "ï")\
            .replace("Ã«", "ë").replace("Ãœ", "Ü").replace("Ã‡", "Ç").replace("Ã§", "ç").replace("Ã‹", "Ë")\
            .replace("Ãˆ", "È").replace("Ã´", "ô")
    else:
        return str_doc.replace("Ã©", "é").replace("Ã¢", "â").replace("Ã¨", "è").replace("Ã‰", "É").replace("Â°", "°")\
            .replace("Ã€", "À").replace("ÃŠ", "Ê").replace("Ã»", "û").replace("Ã ", "à").replace("Ã¯", "ï")\
            .replace("Ã«", "ë").replace("Ãœ", "Ü").replace("Ã‡", "Ç").replace("Ã§", "ç").replace("Ã‹", "Ë")\
            .replace("Ãˆ", "È").replace("Ã´", "ô").replace("\n", "")


# Définir la langue si celle-ci n'est pas définie
try:
    match open("data/language.txt").read().replace("\n", ""):
        case "NotSet":
            language = ask_language()
        case "Français":
            language = "fr"
        case "English":
            language = "en"
        case _:
            language = "en"
except FileNotFoundError:
    with open('data/language.txt', 'w') as defaultLanguage:
        defaultLanguage.write("NotSet")
    language = ask_language()

if os.path.exists("data/languages/{}/translations.txt".format(language)):
    # Si la langue existe
    __translations_list__ = decode_text_document(open("data/languages/{}/translations.txt".format(language)).read())\
        .split('\n')

    __translations_list__.insert(0, "This is the translation list")

    # Pour récupérer un élément depuis la liste de traductions, il suffit de faire '__translations_list__[numéro de la
    # ligne dans le fichier]'.

elif os.path.exists("data/languages/en/translations.txt"):
    # Langue par défaut = Anglais
    __translations_list__ = decode_text_document(open("data/languages/en/translations.txt").read()).split('\n')

    __translations_list__.insert(0, "This is the translation list")

else:
    # Pas de traductions
    __translations_list__ = ["There is nothing here :)"]
    messagebox.showerror("Errorno", "The program can't continue because there is no translation files.\n"
                                    "Le programme ne peut pas continuer car il n'y a pas de fichiers de traduction.\n"
                                    "Lo programme pòt pas continuar perçò qu'i a pas de fichièrs de revirada.")
    quit(0)


class Person:
    """ Définit ce qu'est une personne """

    def __init__(self, age_range=None, size_range=None, weight_range=None, genre_in_class="male", profession=None):
        """ Initialisation de la personne"""
        if weight_range is None:
            weight_range = [60, 65]
        if size_range is None:
            size_range = [175, 175]
        if age_range is None:
            age_range = [20, 20]
        try:
            self.age = randint(int(age_range[0]), int(age_range[1]))  # âge en années
            if not -1 < self.age < 120:
                self.age = 20
        except ValueError:
            self.age = 20
        except IndexError:
            self.age = 20

        try:
            self.size = randint(int(size_range[0]), int(size_range[1]))  # taille en centimètres
            if not -1 < self.size < 250:
                self.size = 175
        except ValueError:
            self.size = 175
        except IndexError:
            self.size = 175
        self.size_in_meters = self.size / 100  # taille en mètres

        try:
            self.weight = randint(int(weight_range[0]), int(weight_range[1]))  # taille en centimètres
            if not -1 < self.weight < 300:
                self.weight = 60
        except ValueError:
            self.weight = 60
        except IndexError:
            self.weight = 60

        self.bmi = self.weight / (self.size_in_meters * self.size_in_meters)  # IMC (BMI = Body Mass Index)
        self.genre_in_class = genre_in_class

        # Couleur de cheveux
        if 2 < self.age < random.randint(49, 55):
            if randint(1, 50) == 50:
                self.hairs_color = __translations_list__[40]
            elif randint(1, 50) == 49:
                self.hairs_color = __translations_list__[41]
            elif randint(1, 50) == 48:
                self.hairs_color = ""
            else:
                if os.path.exists("data/languages/" + language + "/HAIRS_COLORS.txt"):
                    with open("data/languages/" + language + "/HAIRS_COLORS.txt", "r+") as hairs_colors_file:
                        hairs_colors_list = hairs_colors_file.readlines()
                        self.hairs_color = random.choice(hairs_colors_list).replace("\n", "")
                        hairs_colors_file.close()
                else:
                    self.last_name = __translations_list__[42]
        elif 2 < self.age:
            if randint(1, 25) == 1:
                self.hairs_color = __translations_list__[43]
            else:
                self.hairs_color = __translations_list__[44]
        else:
            self.hairs_color = ""

        # Couleurs des yeux
        if randint(1, 100) == 1:
            self.eyes = "verrons"
        else:
            self.eyes = "normaux"

        if self.eyes == "normaux":
            if randint(1, 10) == 1:
                self.eyes_color = [__translations_list__[40]]
            elif randint(1, 50) == 2:
                self.eyes_color = [__translations_list__[41]]
            elif randint(1, 100) == 3:
                self.eyes_color = [__translations_list__[45]]
            elif randint(1, 10000) == 1:
                self.eyes_color = [__translations_list__[46]]
            elif randint(1, 2) == 1:
                self.eyes_color = [__translations_list__[47]]
            else:
                self.eyes_color = [__translations_list__[48]]
        else:
            self.eyes_color = ["", ""]
            while self.eyes_color[0] == self.eyes_color[1]:
                if randint(1, 10) == 1:
                    self.eyes_color = [__translations_list__[40]]
                elif randint(1, 50) == 2:
                    self.eyes_color = [__translations_list__[41]]
                elif randint(1, 100) == 3:
                    self.eyes_color = [__translations_list__[45]]
                elif randint(1, 2) == 1:
                    self.eyes_color = [__translations_list__[47]]
                else:
                    self.eyes_color = [__translations_list__[48]]

                if randint(1, 10) == 1:
                    self.eyes_color += [__translations_list__[40]]
                elif randint(1, 50) == 2:
                    self.eyes_color += [__translations_list__[41]]
                elif randint(1, 100) == 3:
                    self.eyes_color += [__translations_list__[45]]
                elif randint(1, 2) == 1:
                    self.eyes_color += [__translations_list__[47]]
                else:
                    self.eyes_color += [__translations_list__[48]]

        # couleur de peau
        if randint(0, 1) == 0:
            self.skin_color = __translations_list__[49]
        elif randint(0, 1) == 1:
            self.skin_color = __translations_list__[50]
        else:
            self.skin_color = __translations_list__[51]

        # Nom de famille
        # Vérification de l'existence du fichier "LAST_NAMES.txt" et choix du nom
        if os.path.exists("data/languages/" + language + "/LAST_NAMES.txt"):
            last_names_list = decode_text_document(open("data/languages/" + language + "/LAST_NAMES.txt", "r+")
                                                   .read()).split("\n")
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
            self.last_name = __translations_list__[52]

        # caractère
        # Vérification de l'existence du fichier "CHARACTERS_LIST.txt" et choix du caractère
        if os.path.exists("data/languages/" + language + "/CHARACTERS_LIST.txt"):
            characters_list = decode_text_document(open("data/languages/" + language + "/CHARACTERS_LIST.txt", "r+")
                                                   .read()).split("\n")
            self.character = random.choice(characters_list)
        else:
            self.character = __translations_list__[97]

        # Prénom
        match genre_in_class:
            case "male":
                # Vérification de l'existence du fichier "MALES_FIRST_NAMES_LIST.txt" et choix du prénom
                if os.path.exists("data/languages/" + language + "/MALES_FIRST_NAMES_LIST.txt"):
                    first_names_list = decode_text_document(open("data/languages/" + language +
                                                                 "/MALES_FIRST_NAMES_LIST.txt", "r+").read()
                                                            ).split('\n')
                    self.first_name = random.choice(first_names_list).replace("\n", "")  # "\n", c'est le retour ligne
                else:
                    self.first_name = __translations_list__[53]
            case "female":
                # Vérification de l'existence du fichier "FEMALES_FIRST_NAMES_LIST.txt" et choix du prénom
                if os.path.exists("data/languages/" + language + "/FEMALES_FIRST_NAMES_LIST.txt"):
                    first_names_list = decode_text_document(open("data/languages/" + language +
                                                                 "/FEMALES_FIRST_NAMES_LIST.txt", "r+").read()
                                                            ).split('\n')
                    self.first_name = random.choice(first_names_list).replace("\n", "")  # "\n", c'est le retour ligne
                else:
                    self.first_name = __translations_list__[54]
            case _:
                self.first_name = __translations_list__[55]

        while self.last_name == self.first_name.upper():  # Si le prénom est le même que le nom
            # Vérification de l'existence du fichier "LAST_NAMES.txt" et choix du nom
            if os.path.exists("data/languages/" + language + "/LAST_NAMES.txt"):
                with open("data/languages/" + language + "/LAST_NAMES.txt", "r+") as last_names_file:
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
                self.last_name = __translations_list__[52]
        self.last_name_list = self.last_name.split("--")

        while self.first_name.upper() in self.last_name_list:
            # Vérification de l'existence du fichier "LAST_NAMES.txt" et choix du nom
            if os.path.exists("data/languages/" + language + "/LAST_NAMES.txt"):
                with open("data/languages/" + language + "/LAST_NAMES.txt", "r+") as last_names_file:
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
                self.last_name = __translations_list__[52]
            self.last_name_list = self.last_name.split("--")

        # Interprétation de l'IMC.
        if 16.5 > self.bmi:
            self.bmi_interpretation = __translations_list__[56]
        elif 16.5 < self.bmi < 18.5:
            self.bmi_interpretation = __translations_list__[57]
        elif 18.5 < self.bmi < 25:
            self.bmi_interpretation = __translations_list__[58]
        elif 25 < self.bmi < 30:
            self.bmi_interpretation = __translations_list__[59]
        elif 30 < self.bmi < 35:
            self.bmi_interpretation = __translations_list__[60]
        elif 35 < self.bmi < 40:
            self.bmi_interpretation = __translations_list__[61]
        else:
            self.bmi_interpretation = __translations_list__[62]

        # Profession
        if profession is None:
            if not randint(1, 10000) == 1:
                if self.age > 62:
                    self.profession = __translations_list__[95]
                elif 21 < self.age < 63:
                    # Vérification de l'existence du fichier "PROFESSIONS.txt" et choix de la profession
                    if os.path.exists("data/languages/" + language + "/PROFESSIONS.txt"):
                        with open("data/languages/" + language + "/PROFESSIONS.txt", "r+") as professions_file:
                            professions_list = professions_file.readlines()
                            professions_file.close()
                            self.profession = random.choice(professions_list).replace("\n", "")
                    else:
                        self.profession = __translations_list__[90]
                elif 17 < self.age < 22:
                    self.profession = __translations_list__[92]
                elif 5 < self.age:
                    self.profession = __translations_list__[93]
                else:
                    if randint(0, 1) == 1 and 3 < self.age:
                        self.profession = __translations_list__[93]
                    else:
                        self.profession = None
            else:
                self.profession = __translations_list__[96]
        else:
            self.profession = profession

    def get_age(self):
        """ Renvoie l'âge de la personne """
        return self.age

    def get_size(self):
        """ Renvoie la taille de la personne en centimètres """
        return self.size

    def get_size_in_meters(self):
        """ Renvoie la taille de la personne en mètres """
        return self.size_in_meters

    def get_weight(self):
        """ Renvoie le poids de la personne """
        return self.weight

    def get_bmi(self):
        """ Renvoie l'IMC de la personne """
        return self.bmi

    def get_bmi_interpretation(self):
        """ Renvoie l'interprétation de l'IMC de la personne.
         À noter que puisque le calcul est différent et très compliqué pour les enfants, la fonction ne renvoie
         rien si la personne est un enfant."""
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

    def get_genre(self):
        """ Renvoie le sexe de la personne """
        return self.genre_in_class

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


def strint(number):
    """ Renvoie le str() d'un int(). Sert en gros à convertir un float() en str() """
    return str(int(number))


def about():
    messagebox.showinfo(__translations_list__[63], __translations_list__[64] + " {}.\n".format(__version__) +
                        __translations_list__[65] + " {}.\n".format(__author__) + __translations_list__[66] + '\n' +
                        __translations_list__[100])


def add_new_created_identity(number):
    """ Ajoute 1 au nombre d'identités créées """
    global number_of_created_identities

    file = open("data/number_of_created_identities.txt", "r+")
    number_of_created_identities = file.readlines()
    file.close()

    number_of_created_identities = number_of_created_identities[0]
    number_of_created_identities = int(number_of_created_identities) + number

    file = open("data/number_of_created_identities.txt", "w")
    file.write(str(number_of_created_identities))
    file.close()


def open_saved_document(name_of_element="Document"):
    """ Ouvre le document à rappeler """
    if os.path.exists(name_of_element):
        try:
            with open(name_of_element, "r") as file:
                person_saved = decode_text_document(file.read()).split("\n")
                file.close()
            person_name = person_saved[1].replace("\n", '') + " " + person_saved[2].replace("\n", '')
            age = person_saved[3].replace("\n", '')
            genre_in_function_open_saved_document = person_saved[4].replace("\n", '')
            skin_color = person_saved[5].replace("\n", '')
            eyes_color = person_saved[6].replace("\n", '').replace('[', '').replace(']', '') + ','
            eyes_color = eyes_color.split(',')
            del eyes_color[-1]
            hairs_color = person_saved[7].replace("\n", '')
            size_in_meters = person_saved[8].replace("\n", '')
            weight = person_saved[9].replace("\n", '')
            bmi = float(person_saved[10].replace("\n", ''))
            bmi_interpretation = person_saved[11].replace("\n", '')
            profession = person_saved[12].replace("\n", '')
            character = person_saved[13].replace("\n", '')
        except IndexError:
            messagebox.showerror("Erreur / Error", __translations_list__[110] + "\nCode d'erreur : / Error code : "
                                 "python.IndexError")
            return "invalidFileError"
        except UnicodeDecodeError:
            messagebox.showerror("Erreur / Error", __translations_list__[110] + "\nCode d'erreur : / Error code : "
                                 "python.UnicodeDecodeError")
            return "invalidFileError"
        except ValueError:
            messagebox.showerror("Erreur / Error", __translations_list__[110] + "\nCode d'erreur : / Error code : "
                                 "python.ValueError")
            return "invalidFileError"

        result_frame = Frame(tabs, bg='palegreen')

        result_label1 = Label(result_frame, text=(person_name + " " + __translations_list__[19] + " " + age + " "
                                                  + __translations_list__[20]) + ",",
                              font=("Tahoma", 12), bg="palegreen")
        result_label1_bis = Label(result_frame, text=(__translations_list__[21] + " " + skin_color + ","),
                                  font=("Tahoma", 12), bg="palegreen")
        result_label1_bis2 = Label(result_frame, text=character, font=("Tahoma", 12), bg="palegreen")

        if profession is not None:
            result_label1_ter = Label(result_frame, text=(__translations_list__[91] + profession + ","),
                                      font=("Tahoma", 12), bg="palegreen")
        else:
            result_label1_ter = Label(result_frame, text='', font=("Tahoma", 12), bg="palegreen")
        
        if len(eyes_color) == 1:
            result_label2 = Label(result_frame, text=(__translations_list__[22] + " "
                                                      + eyes_color[0].replace("'", "") + ","), font=("Tahoma", 12),
                                  bg="palegreen")
        else:
            result_label2 = Label(result_frame, text=(__translations_list__[19] + " " + __translations_list__[67] + " "
                                                      + eyes_color[0].replace("'", "") + " " +
                                                      __translations_list__[68] + " " + eyes_color[1].replace("'", "")
                                                      + ","), font=("Tahoma", 12), bg="palegreen")
        
        if not hairs_color == "":
            result_label3 = Label(result_frame, text=__translations_list__[23] + " " + hairs_color + ",",
                                  font=("Tahoma", 12), bg="palegreen")
        else:
            result_label3 = Label(result_frame, text=__translations_list__[69], font=("Tahoma", 12),
                                  bg="palegreen")
        
        result_label4 = Label(result_frame, text=(__translations_list__[24] + " " + str(size_in_meters) + " "
                                                  + __translations_list__[25] + ","),
                              font=("Tahoma", 12), bg="palegreen")
        result_label5 = Label(result_frame, text=(__translations_list__[26] + " " + str(weight) + " " +
                                                  __translations_list__[27] + ","),
                              font=("Tahoma", 12), bg="palegreen")
        result_label6 = Label(result_frame, text=(__translations_list__[28] + " " + strint(bmi) + "."),
                              font=("Tahoma", 12), bg="palegreen")

        if not bmi_interpretation == "":
            if genre_in_function_open_saved_document == "male":
                result_label7 = Label(result_frame, text=(__translations_list__[29] + " " + bmi_interpretation + "."),
                                      font=("Tahoma", 12), bg="palegreen")
            else:
                result_label7 = Label(result_frame, text=(__translations_list__[30] + " " + bmi_interpretation + "."),
                                      font=("Tahoma", 12), bg="palegreen")
        else:
            result_label7 = Label(result_frame, text="", font=("Tahoma", 12), bg="palegreen")
        
        close_button = Button(result_frame, text=__translations_list__[99], font=("Tahoma", 12), bg="lightgreen",
                              activebackground='#CCEEFF', command=lambda: tabs.forget(result_frame))

        result_label1.pack()
        result_label1_bis.pack()
        result_label1_bis2.pack()
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
        tabs.add(result_frame, text=(__translations_list__[18] + person_saved[0].replace("\n", '') + " - " + filename))
        tabs.select(result_frame)
        return ""
    else:
        messagebox.showerror(__translations_list__[39], __translations_list__[70])
        return ""


def ask_for_document_saved(event=None):
    """ Demande le document à ouvrir. """

    filename = filedialog.askopenfilename(initialdir="saves/", title=__translations_list__[101],
                                          filetypes=(
                                              (__translations_list__[103], "*.person*"),
                                              (__translations_list__[104], "*.*")
                                          ))
    if not filename == "":
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
                if messagebox.askyesno(__translations_list__[106], __translations_list__[107] + "\n" +
                                       __translations_list__[108]):
                    filename = name + ".person"
                else:
                    filename = name
        file = open(filename, "w")
        file.write(str(number_of_created_identities) + "\n")
        file.write(str(person.get_first_name()) + "\n")
        file.write(str(person.get_last_name()) + "\n")
        file.write(str(person.get_age()) + "\n")
        file.write(str(person.get_genre()) + "\n")
        file.write(str(person.get_skin_color()) + "\n")
        file.write(str(person.get_eyes_color()) + "\n")
        file.write(str(person.get_hairs_color()) + "\n")
        file.write(str(person.get_size_in_meters()) + "\n")
        file.write(str(person.get_weight()) + "\n")
        file.write(str(person.get_bmi()) + "\n")
        file.write(str(person.get_bmi_interpretation()) + "\n")
        file.write(str(person.get_profession()) + "\n")
        file.write(str(person.get_character()) + "\n")
        file.close()
        messagebox.showinfo(__translations_list__[37], (__translations_list__[38] + "\n" +
                                                        filename.split("/")[len(filename.split('/')) - 1])
                            )
    except OSError:
        messagebox.showerror("Erreur / Error", __translations_list__[94])


def save_as(person):
    """ Demande le nom de la sauvegarde. """
    filename = filedialog.asksaveasfilename(initialdir="saves/", title=__translations_list__[102],
                                            filetypes=(
                                                (__translations_list__[103], "*.person"),
                                                (__translations_list__[105], "*.*")
                                            ))
    if filename != "":
        save(person, filename)


def reset_data(event=None):
    """ Réinitialise les données """
    global number_of_created_identities
    # demander à l'utilisateur s'il est sûr de réinitialiser les données
    are_you_sure = messagebox.askquestion(__translations_list__[87], __translations_list__[88] + "\n" +
                                          __translations_list__[89], default='yes')
    if are_you_sure == "yes":
        file = open("data/number_of_created_identities.txt", "w")
        file.write("0")
        file.close()
        number_of_created_identities = 0
        try:
            shutil.rmtree("saves")
        except FileNotFoundError:
            pass
        os.mkdir("saves")

        # refonte du .gitignore pour éviter les bugs de git
        git_ignore = open("saves/.gitignore", "w")
        git_ignore.write("*.person\n")
        git_ignore.close()

        messagebox.showinfo(__translations_list__[37], __translations_list__[78])
        with open('data/language.txt', 'w') as default___language:
            default___language.write("NotSet")
    else:
        messagebox.showinfo(__translations_list__[37], __translations_list__[83])


def result(event=None):
    """ Créé l'onglet où la personne est indiquée """
    global genre, age_range_entry, size_range_entry, weight_range_entry, number_of_created_identities
    try:
        add_new_created_identity(1)
    except FileNotFoundError:
        # Fichier manquant : terminer la fonction en affichant une erreur
        messagebox.showerror(__translations_list__[84], __translations_list__[85] + "\n\n" + __translations_list__[86])
        return "FileNotFoundError"
    if genre == "randomize":
        randomized = True
        pseudo_random_number = randint(0, 1)
        if pseudo_random_number == 0:
            genre = "female"
        else:
            genre = "male"
    else:
        randomized = False
    age_range_entered = age_range_entry.get()
    age_range_in_function = age_range_entered.split('.')
    size_range_entered = size_range_entry.get()
    size_range_in_function = size_range_entered.split('.')
    weight_range_entered = weight_range_entry.get()
    weight_range_in_function = weight_range_entered.split('.')
    
    person = Person(age_range_in_function, size_range_in_function, weight_range_in_function, genre)
    person_name = person.get_first_name() + " " + person.get_last_name()
    person_age = person.get_age()
    person_character = person.get_character()
    skin_color = person.get_skin_color()

    result_frame = Frame(tabs, bg='palegreen')

    result_label1 = Label(result_frame, text=(person_name + " " + __translations_list__[19] + " " +
                                              str(person_age) + " " + __translations_list__[20] + ","),
                          font=("Tahoma", 12), bg="palegreen")
    
    result_label1_bis = Label(result_frame, text=(__translations_list__[21] + " " + str(skin_color) +
                                                  ","), font=("Tahoma", 12), bg="palegreen")
    result_label1_bis2 = Label(result_frame, text=str(person_character), font=("Tahoma", 12), bg="palegreen")
    
    if not person.get_profession() is None:
        result_label1_ter = Label(result_frame, text=(__translations_list__[91] + str(person.get_profession() + ",")),
                                  font=("Tahoma", 12), bg="palegreen")
    else:
        result_label1_ter = Label(result_frame, text='', font=("Tahoma", 12), bg="palegreen")
    
    if len(person.get_eyes_color()) == 1:
        result_label2 = Label(result_frame,
                              text=(__translations_list__[22] + " " +
                                    person.get_eyes_color()[0] + ","), font=("Tahoma", 12), bg="palegreen")
    else:
        result_label2 = Label(result_frame,
                              text=(__translations_list__[67] + " " +
                                    person.get_eyes_color()[0] + " " + __translations_list__[68] + " " +
                                    person.get_eyes_color()[1] + ","), font=("Tahoma", 12), bg="palegreen")
    
    if person.get_hairs_color() != "":
        result_label3 = Label(result_frame, text=(__translations_list__[23] + " " + person.get_hairs_color() + ","),
                              font=("Tahoma", 12), bg="palegreen")
    else:
        result_label3 = Label(result_frame, text=__translations_list__[69], font=("Tahoma", 12), bg="palegreen")
    
    result_label4 = Label(result_frame, text=(__translations_list__[24] + " " + str(person.get_size_in_meters())
                                              + " " + __translations_list__[25] + ","),
                          font=("Tahoma", 12), bg="palegreen")
    
    result_label5 = Label(result_frame, text=(__translations_list__[26] + " " + str(person.get_weight()) + " " +
                                              __translations_list__[27] + ","), font=("Tahoma", 12),
                          bg="palegreen")
    
    result_label6 = Label(result_frame, text=(__translations_list__[28] + " " + strint(person.get_bmi()) + "."),
                          font=("Tahoma", 12), bg="palegreen")
    
    if not person.get_bmi_interpretation() == "":
        if genre == "male":
            result_label7 = Label(result_frame, text=(__translations_list__[29] + " " + person.get_bmi_interpretation()
                                                      + "."),
                                  font=("Tahoma", 12), bg="palegreen")
        else:
            result_label7 = Label(result_frame, text=(__translations_list__[30] + " " + person.get_bmi_interpretation()
                                                      + "."),
                                  font=("Tahoma", 12), bg="palegreen")
    else:
        result_label7 = Label(result_frame, text="", font=("Tahoma", 12), bg="palegreen")
    if randomized:
        genre = "randomize"

    save_button = Button(result_frame, text=__translations_list__[31], font=("Tahoma", 12), bg="lightgreen",
                         activebackground='#CCEEFF', command=lambda: save_as(person))
    close_button = Button(result_frame, text=__translations_list__[99], font=("Tahoma", 12), bg="lightgreen",
                          activebackground='#CCEEFF', command=lambda: tabs.forget(result_frame))

    result_label1.pack()
    result_label1_bis.pack()
    result_label1_bis2.pack()
    
    try:
        # Compliqué d'être à jour avec les noms d'erreurs dans les différentes versions de Python :P
        try:
            result_label1_ter.pack()
        except UnboundLocalError:
            pass
        finally:
            pass
    except NameError:
        try:
            result_label1_ter.pack()
        except NameError:
            pass
        finally:
            pass
    finally:
        pass
    
    result_label2.pack()
    result_label3.pack()
    result_label4.pack()
    result_label5.pack()
    result_label6.pack()
    result_label7.pack()
    save_button.pack()
    close_button.pack()
    tabs.add(result_frame, text=__translations_list__[18] + str(number_of_created_identities))
    tabs.select(result_frame)
    
    all_tabs = list(tabs.tabs())[1:]
    if len(all_tabs) > 200:
        messagebox.showerror("Ban", "You was banned from PersonCraft for reason : autoclick")


def change_to_male():
    """ Mets genre à "male" """
    global genre
    genre = "male"


def change_to_female():
    """ Mets genre à "female" """
    global genre
    genre = "female"


def randomize_genre():
    """ Randomise le genre """
    global genre
    genre = "randomize"


def close_all_tabs(event=None):
    """ Ferme tous les onglets """
    global tabs
    all_tabs = list(tabs.tabs())[1:]  # on enlève l'accueil
    
    for tab in all_tabs:
        tabs.forget(tab)


save_window = Tk()
number_of_created_identities = 0
save_window.destroy()


# Création de la fenêtre
main_window = Tk()
main_window.title(__translations_list__[2])
# ligne suivante : j'utilise cette trad pour vérifier que les caractères sont correctement décodés.
# Dé-commenter en cas de besoin.
# print(__translations_list__[2])
main_window.geometry("900x500")
main_window.minsize(900, 500)
try:
    main_window.iconbitmap('icon.ico')
except TclError:
    pass
main_window.config(background='palegreen')

tabs = ttk.Notebook(main_window)

# Création d'une frame
frame1 = Frame(tabs, bg='palegreen')

tabs.add(frame1, text=__translations_list__[98])
tabs.pack(expand=1, fill="both")

# Création du titre et de texte
title_label = Label(frame1, text=__translations_list__[2], font=('Tahoma', 40), bg='palegreen')
label1 = Label(frame1, text=" ", font=('Tahoma', 15), bg='palegreen')

# Sexe
genre_label = Label(frame1, text=__translations_list__[3], font=('Tahoma', 15), bg='palegreen')
genre = "randomize"
genre_radiobuttons = IntVar()
genre_randomize_radio = Radiobutton(frame1, text=__translations_list__[6], variable=genre_radiobuttons, bg='palegreen',
                                    activebackground='palegreen', value=0, command=lambda: randomize_genre())
genre_female_radio = Radiobutton(frame1, text=__translations_list__[5], variable=genre_radiobuttons, bg='palegreen',
                                 activebackground='palegreen', value=1, command=lambda: change_to_female())
genre_male_radio = Radiobutton(frame1, text=__translations_list__[4], variable=genre_radiobuttons, bg='palegreen',
                               activebackground='palegreen', value=2, command=lambda: change_to_male())

# Tranche d'âge
age_label = Label(frame1, text=__translations_list__[7] + __translations_list__[10],
                  font=('Tahoma', 15), bg='palegreen')
age_range_entry = Entry(frame1, bg='lightgreen')

# Tranche de taille
size_label = Label(frame1, text=__translations_list__[8] + __translations_list__[10], font=('Tahoma', 15),
                   bg='palegreen')
size_range_entry = Entry(frame1, bg='lightgreen')

# Tranche de poids
weight_label = Label(frame1, text=__translations_list__[9] + __translations_list__[10], font=('Tahoma', 15),
                     bg='palegreen')
weight_range_entry = Entry(frame1, bg='lightgreen')

# Bouton OK
label2 = Label(frame1, text=" ", font=('Tahoma', 10), bg='palegreen')
OK_button = Button(frame1, text=__translations_list__[11], font=("Tahoma", 10), bg='lightgreen',
                   activebackground='#CCEEFF', command=lambda: result())

# Ajout d'un menu
menu_bar = Menu(main_window)
file_menu = Menu(menu_bar, tearoff=0)
# réinitialiser données
file_menu.add_command(label=__translations_list__[13], command=lambda: reset_data(), accelerator="Ctrl+R")
# ouvrir...
file_menu.add_command(label=__translations_list__[14], command=lambda: ask_for_document_saved(), accelerator="Ctrl+O")
# fermer tous les onglets
file_menu.add_command(label=__translations_list__[109], command=lambda: close_all_tabs(), accelerator="Ctrl+F1")
menu_bar.add_cascade(label=__translations_list__[12], menu=file_menu)
options_menu = Menu(menu_bar, tearoff=0)
# Bouton OK
options_menu.add_command(label=__translations_list__[11], command=lambda: result(),
                         accelerator=__translations_list__[111])
# à propos du programme
options_menu.add_command(label=__translations_list__[16], command=lambda: about())
# quitter le programme
options_menu.add_command(label=__translations_list__[17], command=lambda: quit(0), accelerator="Ctrl+Q")
menu_bar.add_cascade(label=__translations_list__[15], menu=options_menu)
main_window.config(menu=menu_bar)

# Empaquetage
title_label.pack()
label1.pack()
genre_label.pack()
genre_randomize_radio.pack()
genre_female_radio.pack()
genre_male_radio.pack()
age_label.pack()
age_range_entry.pack()
size_label.pack()
size_range_entry.pack()
weight_label.pack()
weight_range_entry.pack()
label2.pack()
OK_button.pack()

main_window.bind('<Control-q>', exit)
main_window.bind('<Control-r>', reset_data)
main_window.bind('<Control-o>', ask_for_document_saved)
main_window.bind('<Control-F1>', close_all_tabs)
main_window.bind('<Return>', result)
main_window.mainloop()
quit(0)

# Merci d'utiliser mon programme :)
