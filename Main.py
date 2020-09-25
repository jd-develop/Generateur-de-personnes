#!/usr/bin/env python3
# Développé par Jean Dubois
# Générateur aléatoire de personnes

from tkinter import *  # Tkinter sert à faire des fenêtres
from tkinter import messagebox  # Pour faire des boîtes de dialogues

import webbrowser  # Sert à ouvrir le navigateur web
import os  # Pour pouvoir vérifier l'existance de fichiers et le type d'OS car ce n'est pas le même fonctionnement d'un
#            OS à l'autre.
import shutil  # Pour traficoter les fichiers

import random  # Pour pouvoir faire du pseudo-aléatoire
from random import randint  # Pour pas avoir à écrire à chaque fois 'random.randint()'


__author__ = "Jean Dubois <jd-dev@laposte.net>"
__version__ = "20w38a"


def ask_language():
    """ Demande la langue à l'utilisateur """
    language_window = Tk()
    language_window.title("Choix de la langue / Choose language")
    language_window.geometry("500x250")
    language_window.minsize(500, 250)
    language_window.maxsize(500, 250)
    language_window.iconbitmap('icon.ico')
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
    language_window.mainloop()
    language_selected = language_variable.get()
    if int(language_default.get()) == 1:
        with open('data/language.txt', 'w') as default_language:
            default_language.write(language_selected)
    if language_selected == "Français":
        return "fr"
    elif language_selected == "English":
        return "en"
    else:
        return "en"


def decode_text_document(str_doc):
    """ Décode les documents texte UTF-8 """
    return str_doc.replace("Ã©", "é").replace("Ã¢", "â").replace("Ã¨", "è").replace("Ã‰", "É").replace("Â°", "°")\
        .replace("Ã€", "À").replace("ÃŠ", "Ê").replace("Ã»", "û").replace("Ã ", "à")


# Définir la langue si celle-ci n'est pas définie
try:
    if open("data/language.txt").read().replace("\n", "") == "NotSet":
        language = ask_language()
    elif open("data/language.txt").read().replace("\n", "") == "Français":
        language = "fr"
    elif open("data/language.txt").read().replace("\n", "") == "English":
        language = "en"
    else:
        language = "en"
    print(open("data/language.txt").read().replace("\n", ""))
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
    messagebox.showerror("Errorno", "The program can't continue because there is no translations files.\n"
                                    "Le programme ne peut pas continer car il n'y a pas de fichier de traductions.\n"
                                    "Lo programme pot pas continuar perqué i a pas de fichiè de traductions.")
    quit(0)


class Person:
    """ Définit ce qu'est qu'une personne """

    def __init__(self, age_range=None, size_range=None, weight_range=None, genre_in_class="male", profession=None):
        """ Initialisation de la personne"""
        if weight_range is None:
            weight_range = [83, 83]
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
                self.size = 83
        except ValueError:
            self.weight = 83
        except IndexError:
            self.weight = 83

        self.bmi = self.weight / (self.size_in_meters * self.size_in_meters)  # IMC (BMI = Body Mass Index)
        self.genre_in_class = genre_in_class

        # Couleur de cheveux
        if 2 < self.age < 60:
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
        # Vérification de l'existance du fichier "LAST_NAMES.txt" et choix du nom
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

        # Prénom
        if genre_in_class == "male":
            # Vérification de l'existance du fichier "MALES_FIRST_NAMES_LIST.txt" et choix du prénom
            if os.path.exists("data/languages/" + language + "/MALES_FIRST_NAMES_LIST.txt"):
                with open("data/languages/" + language + "/MALES_FIRST_NAMES_LIST.txt", "r+") as first_names_file:
                    first_names_list = first_names_file.readlines()
                    self.first_name = random.choice(first_names_list).replace("\n", "")  # "\n", c'est le retour ligne
                    first_names_file.close()
            else:
                self.first_name = __translations_list__[53]
        elif genre_in_class == "female":
            # Vérification de l'existance du fichier "FEMALES_FIRST_NAMES_LIST.txt" et choix du prénom
            if os.path.exists("data/languages/" + language + "/FEMALES_FIRST_NAMES_LIST.txt"):
                with open("data/languages/" + language + "/FEMALES_FIRST_NAMES_LIST.txt", "r+") as first_names_file:
                    first_names_list = first_names_file.readlines()
                    self.first_name = random.choice(first_names_list).replace("\n", "")
                    first_names_file.close()
            else:
                self.first_name = __translations_list__[54]
        else:
            self.first_name = __translations_list__[55]

        while self.last_name == self.first_name.upper():  # Si le prénom est le même que le nom
            # Vérification de l'existance du fichier "LAST_NAMES.txt" et choix du nom
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
            # Vérification de l'existance du fichier "LAST_NAMES.txt" et choix du nom
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
            if self.age > 62:
                self.profession = __translations_list__[95]
            elif 21 < self.age < 63:
                # Vérification de l'existance du fichier "PROFESSIONS.txt" et choix de la profession
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


def strint(number):
    """ Renvoie le str() d'un int(). Sert en gros à convertir un float() en str() """
    return str(int(number))


def about():
    if not sys.platform == "darwin":
        # Darwin = MacOS : un bug dans webbrowser empêche ce module de fonctionner sous MacOS.
        version_file = open("version.txt", "w")
        version_file.write(__translations_list__[64] + "\n")
        version_file.write("{}\n".format(__version__))
        version_file.write(__translations_list__[65] + " {}.\n".format(__author__))
        version_file.close()
        webbrowser.open_new(r"about.html")
    else:
        # Afficher une boîte de dialogue
        messagebox.showinfo(__translations_list__[63], __translations_list__[64] + " {}.\n".format(__version__) +
                            __translations_list__[65] + " {}.\n".format(__author__) + __translations_list__[66])


def add_new_created_identity(number):
    """ Ajoute 1 au nombre d'identitées créees """
    global number_of_created_identities
    file = open("data/number_of_created_identities.txt", "r+")
    number_of_created_identities = file.readlines()
    file.close()
    number_of_created_identities = number_of_created_identities[0]
    number_of_created_identities = int(number_of_created_identities) + number
    file = open("data/number_of_created_identities.txt", "w")
    file.write(str(number_of_created_identities))
    file.close()


def open_document_saved(name_of_element="Document"):
    """ Ouvre le document à rappeler """
    if os.path.exists("saves/{}.txt".format(name_of_element)):
        with open("saves/{}.txt".format(name_of_element), "r") as file:
            person_saved = file.readlines()
            file.close()

        person_name = person_saved[1].replace("\n", '') + " " + person_saved[2].replace("\n", '')
        age = person_saved[3].replace("\n", '')
        genre_in_function_open_document_saved = person_saved[4].replace("\n", '')
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

        result_window = Tk()
        result_window.title(__translations_list__[18] + person_saved[0])
        result_window.geometry("500x250")
        result_window.minsize(500, 250)
        result_window.maxsize(500, 250)
        result_window.iconbitmap('icon.ico')
        result_window.config(background='palegreen')

        result_label1 = Label(result_window, text=(person_name + " " + __translations_list__[19] + " " + age + " "
                                                   + __translations_list__[20]) + ",",
                              font=("Tahoma", 12), bg="palegreen")
        if not profession is None:
            result_label1_ter = Label(result_window, text=(__translations_list__[91] + profession + ","),
                                      font=("Tahoma", 12), bg="palegreen")
        result_label1_bis = Label(result_window, text=(__translations_list__[21] + " " + skin_color + ","),
                                  font=("Tahoma", 12), bg="palegreen")
        if len(eyes_color) == 1:
            result_label2 = Label(result_window, text=(__translations_list__[19] + " " + __translations_list__[22] + " "
                                                       + eyes_color[0].replace("'", "") + ","), font=("Tahoma", 12),
                                  bg="palegreen")
        else:
            result_label2 = Label(result_window, text=(__translations_list__[19] + " " + __translations_list__[67] + " "
                                                       + eyes_color[0].replace("'", "") + " " +
                                                       __translations_list__[68] + " " + eyes_color[1].replace("'", "")
                                                       + ","), font=("Tahoma", 12), bg="palegreen")
        if not hairs_color == "":
            result_label3 = Label(result_window, text=__translations_list__[23] + " " + hairs_color + ",",
                                  font=("Tahoma", 12), bg="palegreen")
        else:
            result_label3 = Label(result_window, text=__translations_list__[69], font=("Tahoma", 12),
                                  bg="palegreen")
        result_label4 = Label(result_window, text=(__translations_list__[24] + " " + str(size_in_meters) + " "
                                                   + __translations_list__[25] + ","),
                              font=("Tahoma", 12), bg="palegreen")
        result_label5 = Label(result_window, text=(__translations_list__[26] + " " + str(weight) + " " +
                                                   __translations_list__[27] + ","),
                              font=("Tahoma", 12), bg="palegreen")
        result_label6 = Label(result_window, text=(__translations_list__[28] + " " + strint(bmi) + " " +
                                                   __translations_list__[25] + ","),
                              font=("Tahoma", 12), bg="palegreen")
        if not bmi_interpretation == "":
            if genre_in_function_open_document_saved == "male":
                result_label7 = Label(result_window, text=(__translations_list__[29] + " " + bmi_interpretation),
                                      font=("Tahoma", 12), bg="palegreen")
            else:
                result_label7 = Label(result_window, text=(__translations_list__[30] + " " + bmi_interpretation),
                                      font=("Tahoma", 12), bg="palegreen")
        else:
            result_label7 = Label(result_window, text="", font=("Tahoma", 12), bg="palegreen")

        result_label1.pack()
        result_label1_bis.pack()
        result_label1_ter.pack()
        result_label2.pack()
        result_label3.pack()
        result_label4.pack()
        result_label5.pack()
        result_label6.pack()
        result_label7.pack()
        result_window.mainloop()
    else:
        messagebox.showerror(__translations_list__[39], __translations_list__[70])


def ask_for_document_saved():
    """ Demande le document à rappeler """

    enter_document_name_window = Tk()
    enter_document_name_window.title(__translations_list__[71])
    enter_document_name_window.geometry("500x125")
    enter_document_name_window.minsize(500, 125)
    enter_document_name_window.maxsize(500, 125)
    enter_document_name_window.iconbitmap('icon.ico')
    enter_document_name_window.config(background='palegreen')

    enter_document_name_label = Label(enter_document_name_window, text=__translations_list__[72],
                                      font=("Tahoma", 12), bg="palegreen")
    enter_document_name_entry = Entry(enter_document_name_window, font=("Tahoma", 12), bg="lightgreen")
    ok_button = Button(enter_document_name_window, text=__translations_list__[73], font=("Tahoma", 12),
                       bg="lightgreen", activebackground='#CCEEFF',
                       command=lambda: open_document_saved(enter_document_name_entry.get()))
    cancel_button = Button(enter_document_name_window, text=__translations_list__[36], font=("Tahoma", 12),
                           bg="lightgreen", activebackground='#CCEEFF',
                           command=lambda: enter_document_name_window.destroy())

    enter_document_name_label.pack()
    enter_document_name_entry.pack()
    ok_button.pack()
    cancel_button.pack()

    enter_document_name_window.mainloop()


def save(name="Document"):
    """ Sauvegarde """
    global save_window, person

    try:
        if os.path.exists("saves"):
            if not os.path.exists("saves/{}.txt".format(name)):
                file = open("saves/{}.txt".format(name), "w")
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
                file.close()
            else:
                overwrite = messagebox.askquestion(__translations_list__[74],
                                                   __translations_list__[75] + "\n" + __translations_list__[76]
                                                   )
                if overwrite == "yes":
                    file = open("saves/{}.txt".format(name), "w")
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
                    file.close()
                else:
                    messagebox.showinfo(__translations_list__[37], __translations_list__[77])
                    return "ExistingFileNotOverwritten"
            messagebox.showinfo(__translations_list__[37], __translations_list__[38])
            save_window.destroy()
        else:
            os.mkdir("saves")
            file = open("saves/{}.txt".format(name), "w")
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
            file.close()
            messagebox.showinfo(__translations_list__[37], __translations_list__[38])
            save_window.destroy()
    except OSError:
        messagebox.showerror("Erreur / Error", __translations_list__[94])


def save_as():
    """ Demande le nom de la sauvegarde. """
    global save_window

    # Création d'une fenêtre
    save_window = Tk()
    save_window.title(__translations_list__[32])
    save_window.geometry("500x125")
    save_window.minsize(500, 125)
    save_window.maxsize(500, 125)
    save_window.iconbitmap('icon.ico')
    save_window.config(background='palegreen')

    save_as_label = Label(save_window, text=__translations_list__[33], font=("Tahoma", 12),
                          bg="palegreen")
    save_as_entry = Entry(save_window, font=("Tahoma", 12), bg="lightgreen")
    save_button = Button(save_window, text=__translations_list__[34], font=("Tahoma", 12), bg="lightgreen",
                         activebackground='palegreen', command=lambda: save(save_as_entry.get()))
    cancel_button = Button(save_window, text=__translations_list__[36], font=("Tahoma", 12), bg="lightgreen",
                           activebackground='palegreen', command=lambda: save_window.destroy())

    save_as_label.pack()
    save_as_entry.pack()
    save_button.pack()
    cancel_button.pack()

    save_window.mainloop()


def reset_data():
    """ Réinitialise les données """
    global number_of_created_identities
    are_you_sure = messagebox.askquestion(__translations_list__[87], __translations_list__[88] + "\n" +
                                          __translations_list__[89])
    if are_you_sure == "yes":
        if os.path.exists("data/number_of_created_identities.txt"):
            file = open("data/number_of_created_identities.txt", "w")
            file.write("0")
            file.close()
            number_of_created_identities = 0
            try:
                shutil.rmtree("saves")
            except FileNotFoundError:
                os.mkdir("saves")
            messagebox.showinfo(__translations_list__[37], __translations_list__[78])
            with open('data/language.txt', 'w') as default___language:
                default___language.write("NotSet")
        else:
            create_file = messagebox.askquestion(__translations_list__[39], __translations_list__[79] + "\n" +
                                                 __translations_list__[80], icon='error')
            if create_file == "yes":
                file = open("data/number_of_created_identities.txt", "w")
                file.write("0")
                file.close()
                try:
                    shutil.rmtree("saves")
                except FileNotFoundError:
                    os.mkdir("saves")
                messagebox.showinfo(__translations_list__[37], __translations_list__[81])
            else:
                messagebox.showerror(__translations_list__[39], __translations_list__[82])
            with open('data/language.txt', 'w') as default__language:
                default__language.write("NotSet")
    else:
        messagebox.showinfo(__translations_list__[37], __translations_list__[83])


def result():
    """ Renvoie la fenêtre où la personne est indiquée """
    global genre, age_range_entry, size_range_entry, weight_range_entry, number_of_created_identities, person
    try:
        add_new_created_identity(1)
    except FileNotFoundError:
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

    result_window = Tk()
    result_window.title(__translations_list__[18] + str(number_of_created_identities))
    result_window.geometry("500x250")
    result_window.minsize(500, 250)
    result_window.maxsize(500, 250)
    result_window.iconbitmap('icon.ico')
    result_window.config(background='palegreen')

    result_label1 = Label(result_window, text=(person_name + " " + __translations_list__[19] + " " +
                                               str(person.get_age()) + " " + __translations_list__[20] + ","),
                          font=("Tahoma", 12), bg="palegreen")
    
    result_label1_bis = Label(result_window, text=(__translations_list__[21] + " " + str(person.get_skin_color()) +
                                                   ","), font=("Tahoma", 12), bg="palegreen")
    
    if not person.get_profession() is None:
        result_label1_ter = Label(result_window, text=(__translations_list__[91] + str(person.get_profession() + ",")),
                                  font=("Tahoma", 12), bg="palegreen")
    
    if len(person.get_eyes_color()) == 1:
        result_label2 = Label(result_window, text=(__translations_list__[22] + " " +
                                                   person.get_eyes_color()[0]), font=("Tahoma", 12), bg="palegreen")
    else:
        result_label2 = Label(result_window, text=(__translations_list__[67] + " " +
                                                   person.get_eyes_color()[0] + " " + __translations_list__[68] + " " +
                                                   person.get_eyes_color()[1]), font=("Tahoma", 12), bg="palegreen")
    
    if not person.get_hairs_color() == "":
        result_label3 = Label(result_window, text=(__translations_list__[23] + " " + person.get_hairs_color() + ","),
                              font=("Tahoma", 12), bg="palegreen")
    else:
        result_label3 = Label(result_window, text=__translations_list__[69], font=("Tahoma", 12), bg="palegreen")
    
    result_label4 = Label(result_window, text=(__translations_list__[26] + " " + strint(person.get_size_in_meters()) + " " +
                                               __translations_list__[25]),
                          font=("Tahoma", 12), bg="palegreen")
    
    result_label5 = Label(result_window, text=(__translations_list__[26] + " " + str(person.get_weight()) + " " +
                                               __translations_list__[27]), font=("Tahoma", 12),
                          bg="palegreen")
    
    result_label6 = Label(result_window, text=(__translations_list__[28] + " " + strint(person.get_bmi()) + "."),
                          font=("Tahoma", 12), bg="palegreen")
    
    if not person.get_bmi_interpretation() == "":
        if genre == "male":
            result_label7 = Label(result_window, text=(__translations_list__[29] + " " + person.get_bmi_interpretation() +
                                                       "."),
                                  font=("Tahoma", 12), bg="palegreen")
        else:
            result_label7 = Label(result_window, text=(__translations_list__[30] + " " + person.get_bmi_interpretation() +
                                                       "."),
                                  font=("Tahoma", 12), bg="palegreen")
    else:
        result_label7 = Label(result_window, text="", font=("Tahoma", 12), bg="palegreen")
    if randomized:
        genre = "randomize"

    save_button = Button(result_window, text=__translations_list__[31], font=("Tahoma", 12), bg="lightgreen",
                         activebackground='#CCEEFF', command=lambda: save_as())

    result_label1.pack()
    result_label1_bis.pack()
    
    try:
        """ Compliqué d'être à jour avec les noms d'érreurs dans les différentes versions de Python :P """
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
    result_window.mainloop()


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


save_window = Tk()
number_of_created_identities = 0
person = Person()
save_window.destroy()


# Création de la fenêtre
main_window = Tk()
main_window.title(__translations_list__[2])
main_window.geometry("900x500")
main_window.minsize(900, 500)
main_window.iconbitmap('icon.ico')
main_window.config(background='palegreen')

# Création d'une frame
frame1 = Frame(main_window, bg='palegreen')

# Création du titre et de texte
title_label = Label(frame1, text=__translations_list__[2], font=('Tahoma', 40), bg='palegreen')
label1 = Label(frame1, text=" ", font=('Tahoma', 15), bg='palegreen')

# Sexe
genre_label = Label(frame1, text=__translations_list__[3], font=('Tahoma', 15), bg='palegreen')
genre = "female"
genre_radiobuttons = IntVar()
genre_female_radio = Radiobutton(frame1, text=__translations_list__[5], variable=genre_radiobuttons, bg='palegreen',
                                 activebackground='palegreen', value=0, command=lambda: change_to_female())
genre_male_radio = Radiobutton(frame1, text=__translations_list__[4], variable=genre_radiobuttons, bg='palegreen',
                               activebackground='palegreen', value=1, command=lambda: change_to_male())
genre_randomize_radio = Radiobutton(frame1, text=__translations_list__[6], variable=genre_radiobuttons, bg='palegreen',
                                    activebackground='palegreen', value=2, command=lambda: randomize_genre())

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
file_menu.add_command(label=__translations_list__[13], command=lambda: reset_data())
file_menu.add_command(label=__translations_list__[14], command=lambda: ask_for_document_saved())
menu_bar.add_cascade(label=__translations_list__[12], menu=file_menu)
options_menu = Menu(menu_bar, tearoff=0)
options_menu.add_command(label=__translations_list__[11], command=lambda: result())  # Bouton OK
options_menu.add_command(label=__translations_list__[16], command=lambda: about())  # à propos du programme
options_menu.add_command(label=__translations_list__[17], command=lambda: quit(0))
menu_bar.add_cascade(label=__translations_list__[15], menu=options_menu)
main_window.config(menu=menu_bar)

# Empaquetage
title_label.pack()
label1.pack()
genre_label.pack()
genre_female_radio.pack()
genre_male_radio.pack()
genre_randomize_radio.pack()
age_label.pack()
age_range_entry.pack()
size_label.pack()
size_range_entry.pack()
weight_label.pack()
weight_range_entry.pack()
label2.pack()
OK_button.pack()
frame1.pack(expand=YES)
main_window.mainloop()
quit(0)

# Merci d'utiliser mon programme :)
