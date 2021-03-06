###########

"""
Projet MOPSI 2019-2020 Maxime BRISINGER et Raphael LASRY

Ce fichier a pour but de préparer les FICHIERs csv pour la résolution en nombre
Entiers.

Fichier conforme à la norme PEP8
"""

########### Bibliothèques utiles

import os

# Gestion des données avec un csv

import csv
import pandas as pd

# Gestion des matrices

import numpy as np

########### Remplissage du fichier_dettes.csv à partir du fichier Operations.csv
FICHIER_NOMS = "list_names.csv"
def completer_dettes():
    """
    Permet de passer des opérations effectuées à un fichier de dettes.
    """
    if os.path.exists("Operations.csv"):
       # operations = pd.read_csv("Operations.csv", header=None, index_col=None, sep=",")
        #names = list(np.transpose(operations)[0])
        names = pd.read_csv(FICHIER_NOMS, header=None, index_col=None, sep=",")
        names = list(np.transpose(names)[0])
        operations = pd.read_csv("Operations.csv", index_col=None, sep=",")
        #del names[0]
        liste_names = [["NAME", "VALUE"]]
        for name in names:
            liste_names.append(
                [name, sum(operations[name])]
            )  # On impose ici que les opérations soient telles que la somme des
            # Dépenses sur toutes les personnes soit nulle
        liste_names_df = pd.DataFrame(liste_names)
        if os.path.exists("Dettes.csv"):
            os.remove("Dettes.csv")
        liste_names_df.to_csv("Dettes.csv", index=False, header=False, sep=",")
        return liste_names
    return []



########### Création des fichiers CSV
def integer():
    NAMES = completer_dettes()
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
    
    # os.system("glpsol -m TricountCalculMin1.MOD")
    # os.system("glpsol -m TricountCalculFlowInteger.MOD")
    
    # Création des fourchettes hautes et basses
    
    DETTES = [
        [name, 0, 0] for name in NAMES
    ]  # Le deuxième argument représente la fourchette basse, le premier la fourchette haute
    
    FICHIER = open("Results_integer.csv", "r")
    ROWS = csv.reader(FICHIER)
    
    for row in ROWS:
        for perso in DETTES:
            if perso[0] == row[0]:
                perso[1] += int(float(row[1][:])) #fourchette si il le nique à tous les arrondis (payeur)
                perso[2] += int(float(row[1][:])) + 1 #fourchette si il se fait niquer à tous les arrondis (payeur)
            elif perso[0] == row[2]:
                perso[1] += -int(float(row[1][:])) - 1
                perso[2] += -int(float(row[1][:]))
    
    # print("###########################################")
    # print(DETTES)
    # print("###########################################")
    
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
    
    # print("###########################################")
    # print(Echanges)
    # print("###########################################")
    
    ECHANGES_DF = pd.DataFrame(ECHANGES)
    if os.path.exists("Results_fourchettes.csv"):
        os.remove("Results_fourchettes.csv")
    ECHANGES_DF.to_csv("Results_fourchettes.csv", index=False, header=False, sep=",")
    FICHIER.close()
    
    # os.system("glpsol -m TricountInteger1.MOD")
