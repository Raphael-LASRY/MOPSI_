##################################### 

''' 
Projet MOPSI 2019-2020 Maxime BRISINGER et Raphael LASRY  
Ce fichier a pour but de gérer le site et de lancer les différents fichiers .MOD nécessaire à la résolution du probleme du Tricount
'''

##################################### Bibliothèques utiles

import pandas as pd
import os 
import csv
import numpy as np

##################################### Remplissage du fichier Dettes.csv à partir du fichier Operations.csv

def completer_dettes():
    op = pd.read_csv("Operations.csv",header = None, index_col = None, sep=",")
    Names = list(np.transpose(op)[0])
    op = pd.read_csv("Operations.csv", index_col = None, sep=",")
    del(Names[0])
    L=[["NAME","VALUE"]]
    for name in Names:
        L.append([name,sum(op[name])]) # On impose ici que les opérations soient telles que la somme des dépenses sur toutes les personnes soit nulle
    Ldf = pd.DataFrame(L)
    if (os.path.exists("Dettes.csv")):
        os.remove("Dettes.csv")
    Ldf.to_csv("Dettes.csv", index=False, header=False, sep=",")

##################################### Génération aléatoire de csv et comparaison des deux approches

compteur_ecart_flow = 0
compteur_ecart_trans = 0
Nombre_iterations = 5

def read_csv(commande: str): # On remplit un tableau avec les éléments du csv
    r1 = open(commande, "r", newline='')
    a = csv.reader(r1)
    A = []
    for row in a:
        A.append(row)
    r1.close()
    return A
    
for i in range(Nombre_iterations):
    
    # Nettoyage des anciens fichiers
    
    if (os.path.exists("Results.csv")):
        os.remove("Results.csv")
    if (os.path.exists("Exchanges.csv")):
        os.remove("Exchanges.csv")
    if (os.path.exists("Flow.csv")):
        os.remove("Flow.csv")
    if (os.path.exists("Exchanges2.csv")):
        os.remove("Exchanges2.csv")
    completer_dettes()
    
    # Génération de csv et résolution du problème
    
    os.system("python Generation_aleatoire_csv.py")    
    os.system("glpsol -m TricountCalculMin1.MOD")
    os.system("glpsol -m TricountCalculFlow1.MOD")
    os.system("glpsol -m TricountCalculFlow2.MOD")
    os.system("glpsol -m TricountCalculMin2.MOD")
    
    A = read_csv("Exchanges.csv")
    B = read_csv("Exchanges2.csv")
    if (A[-1]!=B[-1]):
        compteur_nb_trans += 1
        
    C = read_csv("Results.csv")
    D = read_csv("Flow.csv")
    if (C[-1][1]!=D[-1][1]):
        compteur_nb_flow += 1
        
if (compteur_ecart_trans != 0 or compteur_ecart_flow != 0):
    print ("Il y a eu {} écarts en nombre de transactions et {} en flow".format(compteur_ecart_trans,compteur_ecart_flow))
else:
    print("Les deux méthodes donnent le même nombre de transactions")
    
##################################### Résolution du problème en transactions entières

# os.system("glpsol -m TricountCalculMinInteger.MOD")
# os.system("glpsol -m TricountCalculFlowInteger.MOD")
