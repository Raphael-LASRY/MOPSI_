###########

"""
Projet MOPSI 2019-2020 Maxime BRISINGER et Raphael LASRY

Ce fichier a pour but de gérer le site et de lancer les différents fichiers .MOD
nécessaire à la résolution du probleme du Tricount

Fichier conforme à la norme PEP8
"""


########### Bibliothèques utiles

import os
from werkzeug.datastructures import ImmutableMultiDict
import random as rd
import numpy as np
import time

# Gestion des données avec un csv

import csv
import pandas as pd

# Gestion des matrices

import numpy as np

# Gestion de la résolution en nombre entiers

#import test_integer as test_int
from test_integer import completer_dettes as dettes

#import generation aleatoire
from Generation_aleatoire_csv import generer as gene

from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS

APP = Flask(__name__)

########### Génération aléatoire de csv et comparaison des deux approches

COMPTEUR_ECART_FLOW = 0
COMPTEUR_ECART_TRANS = 0
NOMBRE_ITERATIONS = 1

FICHIER_OPERATIONS = "Operations.csv"
FICHIER_NOMS = "list_names.csv"
FICHIER_DETTES = "Dettes.csv"
FICHIER_RESULTATS = "Results.csv"
FICHIER_RESULTATS_ENTIERS = "Results_integer.csv"


def read_csv(fichier: str):
    """
    Permet de remplire un tableau avec les éléments du csv.
    """
    file = open(fichier, "r", newline="")
    file_read = csv.reader(file)
    file_tab = []
    for row in file_read:
        file_tab.append(row)
    file.close()
    return file_tab

def clear_files():
    """
    Permet de travailler sur des fichiers initialement vierges
    """
    if os.path.exists(FICHIER_NOMS):
        os.remove(FICHIER_NOMS)
    if os.path.exists(FICHIER_OPERATIONS):
        os.remove(FICHIER_OPERATIONS)

def nb_ligne(fichier):
    """
    Renvoie le nombre de lignes d'un fichier csv
    """
    f = open(fichier, "r")
    i = 0
    for row in f:
        i +=1
    return i
        
def ecrire_operations(dictionnaire_op,FICHIER_OPERATIONS):
    """
    Ecrit, à partir d'un dictionnaire tel que renvoyé par le site, la ligne (string) dans le fichier correspondant
    """
    montant = float(dictionnaire_op["montant"])
    payeur = dictionnaire_op["payeur"]
    payes = dictionnaire_op["payes"]
    
    names = pd.read_csv(FICHIER_OPERATIONS, header=None, index_col=None, sep=",")
    names_list = list(np.transpose(names)[0])
    
    f = open(FICHIER_OPERATIONS, "r")
    rows = csv.reader(f)
    
    List = []
    for row in rows:
        List.append(row)
    rows0 = List[0]
    
    fichier = open(FICHIER_OPERATIONS, "a")
    fichier.write("\n")
    fichier.write(str(nb_ligne(FICHIER_OPERATIONS)) + ",") #index de l'operation
    
    moyenne = montant / len(payes)
    
    for i in range(1,len(rows0)):
        if rows0[i] == payeur:
            if payeur in payes:
                fichier.write(str(montant - moyenne))
            else:
                fichier.write(str(montant))
        else:
            if rows0[i] in payes:
                fichier.write(str(-moyenne))
            else:
                fichier.write("0")
        if i < len(rows0) - 1:
            fichier.write(",")
    
    fichier.close()

def afficher_dettes(fichier):
    """
    Renvoi les dettes sous forme de dico
    """
    dettes = open(fichier, "r")
    rows = csv.reader(dettes)
    dico_dettes = {}
    i = 0
    for row in rows:
        if i > 0: #pour eviter la premiere ligne
            dico_dettes[row[0]] = round(float(row[1]),2)
        i+=1
    return dico_dettes


@APP.route('/')
def home():
    """
    Permet de creer la page d'accueil.
    """
    names=[]
    clear_files()
    if os.path.exists(FICHIER_NOMS):
        operations = pd.read_csv(FICHIER_NOMS, header=None, index_col=None, sep=",")
        names = list(np.transpose(operations)[0])
        del names[0]
    return render_template("bienvenue.html", noms=names)
    
@APP.route("/add", methods=["POST"])
def add():
    """
    Permet d'ajouter un nom
    """
    new_name = request.form["nom"]  # On récupère les infos de la requete
    if os.path.exists(FICHIER_NOMS):
        fichier = open(FICHIER_NOMS, "a")
        string_to_add = "," + new_name
    else:
        fichier = open(FICHIER_NOMS, "a")
        string_to_add = new_name
    fichier.write(string_to_add)
    fichier.close()
    names = pd.read_csv(FICHIER_NOMS, header=None, index_col=None, sep=",")
    names = list(np.transpose(names)[0])
    liste_noms = []
    
    return render_template("bienvenue.html", noms=names)

@APP.route("/add_op", methods=["POST"])
def add_op():
    """
    Permet d'ajouter un nom
    """
    new_op = request.form  # On récupère les infos de la requete
    
    names = pd.read_csv(FICHIER_NOMS, header=None, index_col=None, sep=",")
    names = list(np.transpose(names)[0])
    print(names)
    
    if os.path.exists(FICHIER_OPERATIONS):
        pass
    else:
        fichier = open(FICHIER_OPERATIONS, "a")
        fichier.write("Index")
        for name in names:
            fichier.write("," + name)
        fichier.close()
        
    dictionnaire_op_ajoutee = {}
    dictionnaire_op_ajoutee["payeur"] = new_op["payeur"]
    dictionnaire_op_ajoutee["payes"] = new_op.getlist("payes")
    dictionnaire_op_ajoutee["montant"] = new_op["montant"]
    
    print(dictionnaire_op_ajoutee)
    
    ecrire_operations(dictionnaire_op_ajoutee, FICHIER_OPERATIONS)
    
    dettes()
    dico_dettes = afficher_dettes(FICHIER_DETTES)
    
    return render_template("bienvenue.html", noms=names, dettes=dico_dettes)

@APP.route("/aleat", methods=["POST"])
def exemple_aleatoire():
    gene()
    
    names = pd.read_csv(FICHIER_OPERATIONS, header=None, index_col=None, sep=",")
    names = list(np.transpose(names)[0])
    del names[0]
    
    dettes()
    dico_dettes = afficher_dettes(FICHIER_DETTES)
    
    fichier = open(FICHIER_NOMS, "a")
    i = 0
    for name in names:
        if i > 0:
            fichier.write("," + name)
        else :
            fichier.write(name)
        i += 1
    fichier.close()
    
    return render_template("bienvenue.html", noms=names, dettes=dico_dettes)

@APP.route("/results", methods=["GET"])
def resultats_classiques():
    if os.path.exists("Results.csv"):
        os.remove("Results.csv")
    if os.path.exists("Exchanges.csv"):
        os.remove("Exchanges.csv")

    # Calcul exact solutions
    t1 = time.time()
    os.system("glpsol -m TricountCalculMin1.MOD")
    os.system("glpsol -m TricountCalculFlow1.MOD")
    t2 = time.time()
    t = round(t2 - t1,3)
    
    resultats = open(FICHIER_RESULTATS, "r")
    rows = csv.reader(resultats)
    liste_remboursements = []
    for row in rows:
        liste_remboursements.append(row[0])
    
    dettes()
    dico_dettes = afficher_dettes(FICHIER_DETTES)
    
    return render_template("resultats_classiques.html", remboursements=liste_remboursements, dettes=dico_dettes, time=t)

@APP.route("/results/flowmin", methods=["GET"])
def resultats_flowmin():
    if os.path.exists("Results.csv"):
        os.remove("Results.csv")
    if os.path.exists("Exchanges.csv"):
        os.remove("Exchanges.csv")

    # Calcul exact solutions
    t1= time.time()
    os.system("glpsol -m TricountCalculFlow2.MOD")
    os.system("glpsol -m TricountCalculMin2.MOD")
    t2 = time.time()
    t = round(t2 - t1,3)
    
    resultats = open(FICHIER_RESULTATS, "r")
    rows = csv.reader(resultats)
    liste_remboursements = []
    for row in rows:
        liste_remboursements.append(row[0])
    
    dettes()
    dico_dettes = afficher_dettes(FICHIER_DETTES)
    
    return render_template("resultats_classiques.html", remboursements=liste_remboursements, dettes=dico_dettes, time=t)

@APP.route("/results/entiers", methods=["GET"])
def resultats_entiers():
    NAMES = dettes()
    
    if os.path.exists("Results.csv"):
        os.remove("Results.csv")
    if os.path.exists("Exchanges.csv"):
        os.remove("Exchanges.csv")
    if os.path.exists("Results_integer.csv"):
        os.remove("Results_integer.csv")

    FICHIER = open("Results_integer.csv", "a")
    FICHIER.write("NAMEPAY,SUM,NAMEPAYED \n")
    FICHIER.close()

    # Calcul exact solutions    
    t1 = time.time()
    os.system("glpsol -m TricountCalculMin1.MOD")
    os.system("glpsol -m TricountCalculFlowInteger.MOD")
    
    # Création des fourchettes hautes et basses
    DETTES = [
        [name, 0, 0] for name in NAMES
    ]  # Le deuxième argument représente la fourchette basse, le premier la fourchette haute
    
    FICHIER = open("Results_integer.csv", "r")
    ROWS = csv.reader(FICHIER)
    
    for row in ROWS:
        for perso in DETTES:
            if perso[0] == row[0]:
                perso[1] += int(float(row[1][:]))
                perso[2] += int(float(row[1][:])) + 1
            elif perso[0] == row[2]:
                perso[1] += -int(float(row[1][:])) - 1
                perso[2] += -int(float(row[1][:]))
    
    DETTES_DF = pd.DataFrame(DETTES)
    
    if os.path.exists("Dettes_fourchettes.csv"):
        os.remove("Dettes_fourchettes.csv")
    DETTES_DF.to_csv("Dettes_fourchettes.csv", index=False, header=False, sep=",")
    FICHIER.close()
    
    
    ECHANGES = [["NAMEPAY", "NAMEPAYED", "SUMREAL", "SUMLOW", "SUMHIGH"]]
    FICHIER = open("Results_integer.csv", "r")
    RESULTS = csv.reader(FICHIER)
    
    for row in RESULTS:
        if row[0] != "NAMEPAY":
            ECHANGES.append(
                [
                    row[0],
                    row[2],
                    float(row[1][:]),
                    int(float(row[1][:])),
                    int(float(row[1][:])) + 1,
                ]
            )
    
    ECHANGES_DF = pd.DataFrame(ECHANGES)
    if os.path.exists("Results_fourchettes.csv"):
        os.remove("Results_fourchettes.csv")
    ECHANGES_DF.to_csv("Results_fourchettes.csv", index=False, header=False, sep=",")
    FICHIER.close()
    
    os.system("glpsol -m TricountInteger1.MOD")
    t2 = time.time()
    t = round(t2 - t1,3)

    resultats = open(FICHIER_RESULTATS_ENTIERS, "r")
    rows = csv.reader(resultats)
    
    liste_remboursements_effectifs = []
    liste_ecarts =[]
    somme_ecart = ""
    
    i = 0
    for row in rows:
        if row != [] and i > 3 :
            if row[0][:7] == "L'ecart":
                liste_ecarts.append(row[0])
            elif row[0][:8] == "La somme":
                somme_ecart = row[0]
            else :
                liste_remboursements_effectifs.append(row[0])
        i += 1
    
    dettes()
    dico_dettes = afficher_dettes(FICHIER_DETTES)
    
    return render_template("resultats_entiers.html", remboursements=liste_remboursements_effectifs, ecarts=liste_ecarts, ecart=somme_ecart, dettes=dico_dettes, time=t)

if __name__ == "__main__":
    APP.debug = False
    APP.run()