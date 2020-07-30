#!/usr/bin/env python3
# Développé par Jean Dubois
# Générateur aléatoire de personnes

from tkinter import *  # Tkinter sert à faire des fenêtres
from tkinter import messagebox  # Pour faire des boîtes de dialogues

import webbrowser  # Sert à ouvrir le navigateur web
import os  # Pour pouvoir vérifier l'existance de fichiers
import shutil  # Pour traficoter les fichiers

import random  # Pour pouvoir faire du pseudo-aléatoire
from random import randint  # Pour pas avoir à écrire à chaque fois 'random.randint()'


__author__ = "Jean Dubois <jd-dev@laposte.net>"
__version__ = "1:2i20 InDev Development Version"


class Person:
    """ Définit ce qu'est qu'une personne """

    def __init__(self, age_range=None, size_range=None, weight_range=None, genre_in_class="male"):
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
                self.hairs_color = "bleus"
            elif randint(1, 50) == 49:
                self.hairs_color = "verts"
            elif randint(1, 50) == 48:
                self.hairs_color = ""
            else:
                if os.path.exists("data/HAIRS_COLORS.txt"):
                    with open("data/HAIRS_COLORS.txt", "r+") as hairs_colors_file:
                        hairs_colors_list = hairs_colors_file.readlines()
                        self.hairs_color = random.choice(hairs_colors_list).replace("\n", "")
                        hairs_colors_file.close()
                else:
                    self.last_name = "chatains"
        elif 2 < self.age:
            if randint(1, 25) == 1:
                self.hairs_color = "gris"
            else:
                self.hairs_color = "blancs"
        else:
            self.hairs_color = ""

        # Couleurs des yeux
        if randint(1, 100) == 1:
            self.eyes = "verrons"
        else:
            self.eyes = "normaux"

        if self.eyes == "normaux":
            if randint(1, 10) == 1:
                self.eyes_color = ["bleus"]
            elif randint(1, 50) == 2:
                self.eyes_color = ["verts"]
            elif randint(1, 100) == 3:
                self.eyes_color = ["verts émeraude"]
            elif randint(1, 10000) == 1:
                self.eyes_color = ["crevés"]
            elif randint(1, 2) == 1:
                self.eyes_color = ["noirs"]
            else:
                self.eyes_color = ["chatains"]
        else:
            self.eyes_color = ["", ""]
            while self.eyes_color[0] == self.eyes_color[1]:
                if randint(1, 10) == 1:
                    self.eyes_color = ["bleus"]
                elif randint(1, 50) == 2:
                    self.eyes_color = ["verts"]
                elif randint(1, 100) == 3:
                    self.eyes_color = ["verts émeraude"]
                elif randint(1, 2) == 1:
                    self.eyes_color = ["noirs"]
                else:
                    self.eyes_color = ["chatains"]

                if randint(1, 10) == 1:
                    self.eyes_color += ["bleus"]
                elif randint(1, 50) == 2:
                    self.eyes_color += ["verts"]
                elif randint(1, 100) == 3:
                    self.eyes_color += ["verts émeraude"]
                elif randint(1, 2) == 1:
                    self.eyes_color += ["noirs"]
                else:
                    self.eyes_color += ["chatains"]

        if randint(0, 1) == 0:
            self.skin_color = "blanche"
        elif randint(0, 1) == 1:
            self.skin_color = "noire"
        else:
            self.skin_color = "metis"

        # Nom de famille
        # Vérification de l'existance du fichier "LAST_NAMES.txt" et choix du nom
        if os.path.exists("data/LAST_NAMES.txt"):
            with open("data/LAST_NAMES.txt", "r+") as last_names_file:
                last_names_list = last_names_file.readlines()
                last_names_file.close()
                if randint(1, 10) == 1:
                    self.last_name = random.choice(last_names_list).replace("\n", "") + "--" +\
                                     random.choice(last_names_list).replace("\n", "")
                else:
                    self.last_name = random.choice(last_names_list).replace("\n", "")

        else:
            self.last_name = "DUPOND"

        # Prénom
        if genre_in_class == "male":
            # Vérification de l'existance du fichier "MALES_FIRST_NAMES_LIST.txt" et choix du prénom
            if os.path.exists("data/MALES_FIRST_NAMES_LIST.txt"):
                with open("data/MALES_FIRST_NAMES_LIST.txt", "r+") as first_names_file:
                    first_names_list = first_names_file.readlines()
                    self.first_name = random.choice(first_names_list).replace("\n", "")  # "\n", c'est le retour ligne
                    first_names_file.close()
            else:
                self.first_name = "Pierre"
        elif genre_in_class == "female":
            # Vérification de l'existance du fichier "FEMALES_FIRST_NAMES_LIST.txt" et choix du prénom
            if os.path.exists("data/FEMALES_FIRST_NAMES_LIST.txt"):
                with open("data/FEMALES_FIRST_NAMES_LIST.txt", "r+") as first_names_file:
                    first_names_list = first_names_file.readlines()
                    self.first_name = random.choice(first_names_list).replace("\n", "")
                    first_names_file.close()
            else:
                self.first_name = "Marie"
        else:
            self.first_name = "Dominique"

        while self.last_name == self.first_name.upper():  # Si le prénom est égal au nom
            # Vérification de l'existance du fichier "LAST_NAMES.txt" et choix du nom
            if os.path.exists("data/LAST_NAMES.txt"):
                with open("data/LAST_NAMES.txt", "r+") as last_names_file:
                    last_names_list = last_names_file.readlines()
                    last_names_file.close()
                    if randint(1, 10) == 1:
                        self.last_name = random.choice(last_names_list).replace("\n", "") + "--" + \
                                         random.choice(last_names_list).replace("\n", "")
                    else:
                        self.last_name = random.choice(last_names_list).replace("\n", "")

            else:
                self.last_name = "DUPOND"

        if 16.5 > self.bmi:
            self.bmi_interpretation = "famine"
        elif 16.5 < self.bmi < 18.5:
            self.bmi_interpretation = "maigreur"
        elif 18.5 < self.bmi < 25:
            self.bmi_interpretation = "corpulence normale"
        elif 25 < self.bmi < 30:
            self.bmi_interpretation = "surpoids"
        elif 30 < self.bmi < 35:
            self.bmi_interpretation = "obésité modérée"
        elif 35 < self.bmi < 40:
            self.bmi_interpretation = "obésité sévère"
        else:
            self.bmi_interpretation = "obésité morbide"

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


def about():
    version_file = open("version.txt", "w")
    version_file.write("Générateur de personnes, version\n")
    version_file.write("{}\n".format(__version__))
    version_file.write("Développé par {}.\n".format(__author__))
    version_file.close()
    webbrowser.open_new(r"about.html")


def add_new_created_identity(number):
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

        result_window = Tk()
        result_window.title("Identité créée n°{}".format(person_saved[0]))
        result_window.geometry("500x250")
        result_window.minsize(500, 250)
        result_window.maxsize(500, 250)
        result_window.iconbitmap('icon.ico')
        result_window.config(background='palegreen')

        result_label1 = Label(result_window, text=person_name + " a {} ans,".format(age),
                              font=("Tahoma", 12), bg="palegreen")
        result_label1_bis = Label(result_window, text="a la peau {},".format(skin_color),
                                  font=("Tahoma", 12), bg="palegreen")
        if len(eyes_color) == 1:
            result_label2 = Label(result_window, text="les yeux {}".format(eyes_color[0]),
                                  font=("Tahoma", 12), bg="palegreen")
        else:
            result_label2 = Label(result_window, text="a les yeux verron {} et ".format(eyes_color[0])
                                                      + person.get_eyes_color()[1], font=("Tahoma", 12), bg="palegreen")
        if not hairs_color == "":
            result_label3 = Label(result_window, text="et les cheveux {},".format(hairs_color),
                                  font=("Tahoma", 12), bg="palegreen")
        else:
            result_label3 = Label(result_window, text="et aucun cheveu sur la tête,", font=("Tahoma", 12),
                                  bg="palegreen")
        result_label4 = Label(result_window, text="fait {} mètres, ".format(size_in_meters),
                              font=("Tahoma", 12), bg="palegreen")
        result_label5 = Label(result_window, text="pèse {} kilogrammes, ".format(weight),
                              font=("Tahoma", 12), bg="palegreen")
        result_label6 = Label(result_window, text="a une IMC d'environ {}.".format(int(bmi)),
                              font=("Tahoma", 12), bg="palegreen")
        if not bmi_interpretation == "":
            if genre_in_function_open_document_saved == "male":
                result_label7 = Label(result_window, text="Il est donc en {}.".format(bmi_interpretation),
                                      font=("Tahoma", 12), bg="palegreen")
            else:
                result_label7 = Label(result_window,
                                      text="Elle est donc en {}.".format(bmi_interpretation),
                                      font=("Tahoma", 12), bg="palegreen")
        else:
            result_label7 = Label(result_window, text="", font=("Tahoma", 12), bg="palegreen")

        result_label1.pack()
        result_label1_bis.pack()
        result_label2.pack()
        result_label3.pack()
        result_label4.pack()
        result_label5.pack()
        result_label6.pack()
        result_label7.pack()
        result_window.mainloop()
    else:
        messagebox.showerror("Erreur", "Cette sauvegarde n'existe pas, veuillez réessayer.")


def ask_for_document_saved():
    """ Demande le document à rappeler """

    enter_document_name_window = Tk()
    enter_document_name_window.title("Rappel")
    enter_document_name_window.geometry("500x125")
    enter_document_name_window.minsize(500, 125)
    enter_document_name_window.maxsize(500, 125)
    enter_document_name_window.iconbitmap('icon.ico')
    enter_document_name_window.config(background='palegreen')

    enter_document_name_label = Label(enter_document_name_window, text="Nom de la sauvegarde à rappeller :",
                                      font=("Tahoma", 12), bg="palegreen")
    enter_document_name_entry = Entry(enter_document_name_window, font=("Tahoma", 12), bg="lightgreen")
    ok_button = Button(enter_document_name_window, text="OK", font=("Tahoma", 12), bg="lightgreen",
                       activebackground='#B0F2B6', command=lambda: open_document_saved(enter_document_name_entry.get()))
    cancel_button = Button(enter_document_name_window, text="Annuler", font=("Tahoma", 12), bg="lightgreen",
                           activebackground='#B0F2B6', command=lambda: enter_document_name_window.destroy())

    enter_document_name_label.pack()
    enter_document_name_entry.pack()
    ok_button.pack()
    cancel_button.pack()

    enter_document_name_window.mainloop()


def save(name="Document"):
    """ Sauvegarde """
    global save_window, person

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
            file.close()
        else:
            overwrite = messagebox.askquestion("Écraser ?", "Une sauvegarde portant ce nom existe déjà.\n"
                                                            "Voulez-vous l'écraser ?")
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
                file.close()
            else:
                messagebox.showinfo("Information", "Non sauvegardé.")
                return "ExistantFileNotOverwrited"
        messagebox.showinfo("Information", "Sauvegardé avec succès !")
        save_window.destroy()
    else:
        os.mkdir("saves")
        file = open("saves/{}.txt".format(name), "w")
        file.write(str(person.get_first_name()) + "\n")
        file.write(str(person.get_last_name()) + "\n")
        file.write(str(person.get_genre()) + "\n")
        file.write(str(person.get_skin_color()) + "\n")
        file.write(str(person.get_eyes_color()) + "\n")
        file.write(str(person.get_hairs_color()) + "\n")
        file.write(str(person.get_size_in_meters()) + "\n")
        file.write(str(person.get_weight()) + "\n")
        file.write(str(person.get_bmi()) + "\n")
        file.write(str(person.get_bmi_interpretation()) + "\n")
        file.close()
        messagebox.showinfo("Information", "Sauvegardé avec succès !")
        save_window.destroy()


def save_as():
    """ Demande le nom de la sauvegarde. """
    global save_window

    # Création d'une fenêtre
    save_window = Tk()
    save_window.title("Sauvegarder sous...")
    save_window.geometry("500x125")
    save_window.minsize(500, 125)
    save_window.maxsize(500, 125)
    save_window.iconbitmap('icon.ico')
    save_window.config(background='palegreen')

    save_as_label = Label(save_window, text="Enregistrer sous : (entrez le nom de la sauvegarde)", font=("Tahoma", 12),
                          bg="palegreen")
    save_as_entry = Entry(save_window, font=("Tahoma", 12), bg="lightgreen")
    save_button = Button(save_window, text="Sauvegarder", font=("Tahoma", 12), bg="lightgreen",
                         activebackground='#B0F2B6', command=lambda: save(save_as_entry.get()))
    cancel_button = Button(save_window, text="Annuler", font=("Tahoma", 12), bg="lightgreen",
                           activebackground='#B0F2B6', command=lambda: save_window.destroy())

    save_as_label.pack()
    save_as_entry.pack()
    save_button.pack()
    cancel_button.pack()

    save_window.mainloop()


def reset_data():
    """ Réinitialise les données """
    global number_of_created_identities
    are_you_sure = messagebox.askquestion("Confirmation", "Êtes-vous sûr(e) de vouloir réinitialiser les données ?\n"
                                                          "Cette action est irréversible.")
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
            messagebox.showinfo("Information", "Données réinitialisées avec succès !")
        else:
            create_file = messagebox.askquestion("Erreur", "Un fichier est manquant.\n"
                                                           "Voulez-vous le créer ?", icon='error')
            if create_file == "yes":
                file = open("data/number_of_created_identities.txt", "w")
                file.write("0")
                file.close()
                try:
                    shutil.rmtree("saves")
                except FileNotFoundError:
                    os.mkdir("saves")
                messagebox.showinfo("Information", "Fichier manquant crée avec succès !")
            else:
                messagebox.showerror("Erreur", "Impossible de réinitialiser les données : un fichier est manquant.")
    else:
        messagebox.showinfo("Information", "Données non réinitialisées.")


def result():
    """ Renvoie la fenêtre où la personne est indiquée """
    global genre, age_range_entry, size_range_entry, weight_range_entry, number_of_created_identities, person
    try:
        add_new_created_identity(1)
    except FileNotFoundError:
        messagebox.showerror("FileNotFoundError", "Le programme ne peut pas continuer car le fichier 'number_of_creat"
                                                  "ed_identities.txt' n'existe pas.\n\n Veuillez réinitialiser les"
                                                  "données (menu 'Options'>'Réinitialiser les données') afin de le crée"
                                                  "r et de corriger l'érreur.")
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
    result_window.title("Identité créée n°{}".format(number_of_created_identities))
    result_window.geometry("500x250")
    result_window.minsize(500, 250)
    result_window.maxsize(500, 250)
    result_window.iconbitmap('icon.ico')
    result_window.config(background='palegreen')

    result_label1 = Label(result_window, text=person_name + " a {} ans,".format(person.get_age()), font=("Tahoma", 12),
                          bg="palegreen")
    result_label1_bis = Label(result_window, text="a la peau {},".format(person.get_skin_color()), font=("Tahoma", 12),
                              bg="palegreen")
    if len(person.get_eyes_color()) == 1:
        result_label2 = Label(result_window, text="les yeux {}".format(person.get_eyes_color()[0]),
                              font=("Tahoma", 12), bg="palegreen")
    else:
        result_label2 = Label(result_window, text="a les yeux verron {} et ".format(person.get_eyes_color()[0])
                                                  + person.get_eyes_color()[1], font=("Tahoma", 12), bg="palegreen")
    if not person.get_hairs_color() == "":
        result_label3 = Label(result_window, text="et les cheveux {},".format(person.get_hairs_color()),
                              font=("Tahoma", 12), bg="palegreen")
    else:
        result_label3 = Label(result_window, text="et aucun cheveu sur la tête,", font=("Tahoma", 12), bg="palegreen")
    result_label4 = Label(result_window, text="fait {} mètres, ".format(person.get_size_in_meters()),
                          font=("Tahoma", 12), bg="palegreen")
    result_label5 = Label(result_window, text="pèse {} kilogrammes, ".format(person.get_weight()), font=("Tahoma", 12),
                          bg="palegreen")
    result_label6 = Label(result_window, text="a une IMC d'environ {}.".format(int(person.get_bmi())),
                          font=("Tahoma", 12), bg="palegreen")
    if not person.get_bmi_interpretation() == "":
        if genre == "male":
            result_label7 = Label(result_window, text="Il est donc en {}.".format(person.get_bmi_interpretation()),
                                  font=("Tahoma", 12), bg="palegreen")
        else:
            result_label7 = Label(result_window, text="Elle est donc en {}.".format(person.get_bmi_interpretation()),
                                  font=("Tahoma", 12), bg="palegreen")
    else:
        result_label7 = Label(result_window, text="", font=("Tahoma", 12), bg="palegreen")
    if randomized:
        genre = "randomize"

    save_button = Button(result_window, text="Sauvegarder...", font=("Tahoma", 12), bg="lightgreen",
                         activebackground='#B0F2B6', command=lambda: save_as())

    result_label1.pack()
    result_label1_bis.pack()
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
main_window.title("Générateur aléatoire de personnes")
main_window.geometry("900x500")
main_window.minsize(900, 500)
main_window.iconbitmap('icon.ico')
main_window.config(background='palegreen')

# Création d'une frame
frame1 = Frame(main_window, bg='palegreen')

# Création du titre et de texte
title_label = Label(frame1, text="Générateur aléatoire de personnes", font=('Tahoma', 40), bg='palegreen')
label1 = Label(frame1, text=" ", font=('Tahoma', 15), bg='palegreen')

# Sexe
genre_label = Label(frame1, text="Sexe : ", font=('Tahoma', 15), bg='palegreen')
genre = "female"
genre_radiobuttons = IntVar()
genre_female_radio = Radiobutton(frame1, text="Féminin", variable=genre_radiobuttons, bg='palegreen',
                                 activebackground='palegreen', value=0, command=lambda: change_to_female())
genre_male_radio = Radiobutton(frame1, text="Masculin", variable=genre_radiobuttons, bg='palegreen',
                               activebackground='palegreen', value=1, command=lambda: change_to_male())
genre_randomize_radio = Radiobutton(frame1, text="Randomiser", variable=genre_radiobuttons, bg='palegreen',
                                    activebackground='palegreen', value=2, command=lambda: randomize_genre())

# Tranche d'âge
age_label = Label(frame1, text="Tranche d'age (séparer par un point) : ", font=('Tahoma', 15), bg='palegreen')
age_range_entry = Entry(frame1, bg='lightgreen')

# Tranche de taille
size_label = Label(frame1, text="Tranche de taille en centimètres (séparer par un point) : ", font=('Tahoma', 15),
                   bg='palegreen')
size_range_entry = Entry(frame1, bg='lightgreen')

# Tranche de poids
weight_label = Label(frame1, text="Tranche de poids en kilogrammes (séparer par un point) : ", font=('Tahoma', 15),
                     bg='palegreen')
weight_range_entry = Entry(frame1, bg='lightgreen')

# Bouton OK
label2 = Label(frame1, text=" ", font=('Tahoma', 10), bg='palegreen')
OK_button = Button(frame1, text="Soumettre ce formulaire", font=("Tahoma", 10), bg='lightgreen',
                   activebackground='#B0F2B6', command=lambda: result())

# Ajout d'un menu
menu_bar = Menu(main_window)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Réinitialiser les données...', command=lambda: reset_data())
file_menu.add_command(label='Rappel...', command=lambda: ask_for_document_saved())
menu_bar.add_cascade(label='Fichier', menu=file_menu)
options_menu = Menu(menu_bar, tearoff=0)
options_menu.add_command(label='Soumettre ce formulaire', command=lambda: result())  # Bouton OK
options_menu.add_command(label='À propos...', command=lambda: about())  # à propos du programme
options_menu.add_command(label='Quitter', command=lambda: quit(0))
menu_bar.add_cascade(label='Options', menu=options_menu)
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

# Merci d'utiliser mon programme :)
