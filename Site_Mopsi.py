###########

"""
Projet MOPSI 2019-2020 Maxime BRISINGER et Raphael LASRY

Ce fichier a pour but de gérer le site et de lancer les différents fichiers .MOD
nécessaire à la résolution du probleme du Tricount

Fichier conforme à la norme PEP8
"""

########### Bibliothèques utiles

import os

# Gestion des données avec un csv

import csv
import pandas as pd

# Gestion des matrices

import numpy as np

########### Remplissage du fichier Dettes.csv à partir du fichier Operations.csv

def completer_dettes():
    """
    Permet de passer des opérations effectuées à un fichier de dettes.
    """
    operations = pd.read_csv("Operations.csv", header=None, index_col=None, sep=",")
    names = list(np.transpose(operations)[0])
    operations = pd.read_csv("Operations.csv", index_col=None, sep=",")
    del names[0]
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

########### Génération aléatoire de csv et comparaison des deux approches

COMPTEUR_ECART_FLOW = 0
COMPTEUR_ECART_TRANS = 0
NOMBRE_ITERATIONS = 5


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


for i in range(NOMBRE_ITERATIONS):

    # Nettoyage des anciens fichiers

    if os.path.exists("Results.csv"):
        os.remove("Results.csv")
    if os.path.exists("Exchanges.csv"):
        os.remove("Exchanges.csv")
    if os.path.exists("Flow.csv"):
        os.remove("Flow.csv")
    if os.path.exists("Exchanges2.csv"):
        os.remove("Exchanges2.csv")
    completer_dettes()

    # Génération de csv et résolution du problème

    os.system("python Generation_aleatoire_csv.py")
    os.system("glpsol -m TricountCalculMin1.MOD")
    os.system("glpsol -m TricountCalculFlow1.MOD")
    os.system("glpsol -m TricountCalculFlow2.MOD")
    os.system("glpsol -m TricountCalculMin2.MOD")

    file_1 = read_csv("Exchanges.csv")
    file_2 = read_csv("Exchanges2.csv")
    if file_1[-1] != file_2[-1]:
        compteur_nb_trans += 1

    results_1 = read_csv("Results.csv")
    results_2 = read_csv("Flow.csv")
    if results_1[-1][1] != results_2[-1][1]:
        compteur_nb_flow += 1

if COMPTEUR_ECART_TRANS != 0 or COMPTEUR_ECART_FLOW != 0:
    print(
        "Il y a eu {} écarts en nombre de transactions et {} en flow".format(
            COMPTEUR_ECART_TRANS, COMPTEUR_ECART_FLOW
        )
    )
else:
    print("Les deux méthodes donnent le même nombre de transactions")

########### Résolution du problème en transactions entières

# os.system("glpsol -m TricountCalculMinInteger.MOD")
# os.system("glpsol -m TricountCalculFlowInteger.MOD")
