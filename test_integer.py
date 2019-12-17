##################################### 

''' 
Projet MOPSI 2019-2020 Maxime BRISINGER et Raphael LASRY  
Ce fichier a pour but de préparer les csv pour réaliser des transactions entières
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
    return (Names)
Names = completer_dettes()

##################################### Création des fichier Results_integer.csv, Results_fourchettes.csv et Dettes_fourchettes.csv

if (os.path.exists("Results.csv")):
    os.remove("Results.csv")
if (os.path.exists("Exchanges.csv")):
    os.remove("Exchanges.csv")
if (os.path.exists("Results_integer.csv")):
    os.remove("Results_integer.csv")

r = open("Results_integer.csv", "a")
r.write("NAMEPAY,SUM,NAMEPAYED \n")
r.close()

# Calcul exact solutions

os.system("glpsol -m TricountCalculMin1.MOD")
os.system("glpsol -m TricountCalculFlowInteger.MOD")

# Création des fourchettes hautes et basses

Dettes = [[name,0,0] for name in Names] # Le deuxième argument représente la fourchette basse, le premier la fourchette haute
r = open("Results_integer.csv", "r")
Rows = csv.reader(r)

for row in Rows:
    for perso in Dettes:
        if perso[0] == row[0]:
            perso[1] += int(float(row[1][:]))
            perso[2] += int(float(row[1][:])) + 1
        elif perso[0] == row[2]:
            perso[1] += -int(float(row[1][:])) -1
            perso[2] += -int(float(row[1][:]))
            
# print("###########################################")
# print(Dettes)
# print("###########################################")

Dettesdf = pd.DataFrame(Dettes)
if (os.path.exists("Dettes_fourchettes.csv")):
    os.remove("Dettes_fourchettes.csv")
Dettesdf.to_csv("Dettes_fourchettes.csv", index=False, header=False, sep=",")
r.close()




Echanges = [["NAMEPAY","NAMEPAYED","SUMREAL","SUMLOW","SUMHIGH"]]
r = open("Results_integer.csv", "r")
results = csv.reader(r)

for row in results:
    if row[0] != "NAMEPAY":
        Echanges.append([row[0],row[2],float(row[1][:]),int(float(row[1][:])),int(float(row[1][:]))+1])
            
# print("###########################################")
# print(Echanges)
# print("###########################################")

Echangesdf = pd.DataFrame(Echanges)
if (os.path.exists("Results_fourchettes.csv")):
    os.remove("Results_fourchettes.csv")
Echangesdf.to_csv("Results_fourchettes.csv", index=False, header=False, sep=",")
r.close()

res = pd.read_csv("Results_fourchettes.csv", index_col = None, sep=",")

os.system("glpsol -m TricountInteger1.MOD")



