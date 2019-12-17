##################################### 

''' 
Projet MOPSI 2019-2020 Maxime BRISINGER et Raphael LASRY  
Ce fichier a pour but de génerer aléatoirement des transactions
'''

##################################### Bibliothèques utiles

import csv
import random as rd
import numpy as np

##################################### Paramètres

Nombre_utilisateurs = rd.randint(2, 7)
Nombre_operations = rd.randint(1, 5)
somme_max = 20

##################################### Génération aléatoire des transactions

Matrice_operations = np.empty((Nombre_operations, Nombre_utilisateurs))

for i in range(Nombre_operations):
    for j in range(Nombre_utilisateurs):
        Matrice_operations[i, j] = somme_max*rd.random() # On paie entre 0 et somme_max€
for i in range(Nombre_operations):
    Matrice_operations[i] -= np.mean(Matrice_operations[i, :]) # On centre les opérations en fonction du nombre de personnes 

delta = np.zeros(Nombre_operations) # On arrondit les paiements au centime près, il peut donc y avoir un écart
for i in range(Nombre_operations):
    for j in range(Nombre_utilisateurs):
        delta[i] -= round(Matrice_operations[i, j], 2)
        
##################################### Écriture des résultats

r = open("Operations.csv", "w")
r.write("Index,")

for i in range(1, Nombre_utilisateurs + 1):
    r.write("Name" + str(i) + ",")    
r.write("Name" + str(Nombre_utilisateurs + 1))
r.write("\n")

for i in range(Nombre_operations):
    r.write(str(i) + ",")
    for j in range(Nombre_utilisateurs):
        r.write(str(round(Matrice_operations[i, j], 2)))
        r.write(",")
    r.write(str(round(delta[i], 2)))
    r.write("\n")