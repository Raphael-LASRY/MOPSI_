#####################################

"""
Projet MOPSI 2019-2020 Maxime BRISINGER et Raphael LASRY

Ce fichier a pour but de génerer aléatoirement des opérations et les écrire dans
Un csv.

Fichier conforme à la norme PEP8
"""

##################################### Bibliothèques utiles

import random as rd
import numpy as np

def generer():
    ##################################### Paramètres
    
    NOMBRE_UTILISATEURS = rd.randint(2, 7)
    NOMBRE_OPERATIONS = rd.randint(1, 6)
    SOMME_MAX = 20
    
    ##################################### Génération aléatoire des transactions
    
    MATRICE_OPERATIONS = np.empty((NOMBRE_OPERATIONS, NOMBRE_UTILISATEURS))
    
    for i in range(NOMBRE_OPERATIONS):
        for j in range(NOMBRE_UTILISATEURS):
            MATRICE_OPERATIONS[i, j] = (
                SOMME_MAX * rd.random()
            )  # On paie entre 0 et SOMME_MAX€
        MATRICE_OPERATIONS[i] -= np.mean(
            MATRICE_OPERATIONS[i, :]
        )  # On centre les opérations en fonction du nombre de personnes
    
    DELTA = np.zeros(
        NOMBRE_OPERATIONS
    )  # On arrondit les paiements au centime près, il peut donc y avoir un écart
    for i in range(NOMBRE_OPERATIONS):
        for j in range(NOMBRE_UTILISATEURS):
            DELTA[i] -= round(MATRICE_OPERATIONS[i, j], 2)
    
    ##################################### Écriture des résultats
    
    FICHIER = open("Operations.csv", "w")
    FICHIER.write("Index,")
    
    for i in range(1, NOMBRE_UTILISATEURS + 1):
        FICHIER.write("Name" + str(i) + ",")
    FICHIER.write("Name" + str(NOMBRE_UTILISATEURS + 1))
    FICHIER.write("\n")
    
    for i in range(NOMBRE_OPERATIONS):
        FICHIER.write(str(i) + ",")
        for j in range(NOMBRE_UTILISATEURS):
            FICHIER.write(str(round(MATRICE_OPERATIONS[i, j], 2)))
            FICHIER.write(",")
        FICHIER.write(str(round(DELTA[i], 2)))
        FICHIER.write("\n")

generer()