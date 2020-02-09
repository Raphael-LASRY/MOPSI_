from generation_aleatoire_csv import generer as gene
from heuristique import Heuristique as heur
import matplotlib.pyplot as plt
import time
import os
import numpy as np
import csv

Nombre_essais = 5
Temps = np.zeros((3,Nombre_essais))
Argent_echange = np.zeros((3,Nombre_essais))
Nombre_echange = np.zeros((3,Nombre_essais))

for i in range (Nombre_essais):
    gene()

    R = []

    t1 = time.time()
    heur(R)
    t2 = time.time()

    a1 = R[-1][0][-1]
    e1 = R[0][0][1]

    Temps[0][i] = t2-t1
    Argent_echange[0][i] = a1
    Nombre_echange [0][i] = e1

    if os.path.exists("Exchanges.csv"):
        os.remove("Exchanges.csv")
    if os.path.exists("Results.csv"):
        os.remove("Results.csv")
    t3 = time.time()
    os.system("glpsol -m TricountCalculMin1.MOD")
    os.system("glpsol -m TricountCalculFlow1.MOD")
    t4 = time.time()

    resultats = open("Results.csv", "r")
    rows = csv.reader(resultats)
    for row in rows:
        a = row[0]
    j = -1
    a2 = str(a[j])
    while str(a[j]) != " ":
        j-= 1
        a2 += str(a[j])
    a2 = float("".join(reversed(a2)))
    resultats.close()
    
    resultats = open("Exchanges.csv", "r")
    rows = csv.reader(resultats)
    for row in rows:
        a = row[1]
    j = -1
    e2 = str(a[j])
    while str(a[j]) != " ":
        j-= 1
        if len(a) >= -j:
          e2 += str(a[j])
        else:
           break
    e2 = float("".join(reversed(e2)))
    resultats.close()

    Temps[1][i] = t4-t3
    Argent_echange[1][i] = a2
    Nombre_echange[1][i] = int(e2)

    if os.path.exists("Flow.csv"):
        os.remove("Flow.csv")
    if os.path.exists("Exchanges2.csv"):
        os.remove("Exchanges2.csv")
    t5 = time.time()
    os.system("glpsol -m TricountCalculFlow2.MOD")
    os.system("glpsol -m TricountCalculMin2.MOD")
    t6 = time.time()

    resultats = open("Flow.csv", "r")
    rows = csv.reader(resultats)
    for row in rows:
        a = row[1]
    a3 = float(str(a))
    resultats.close()
    
    resultats = open("Exchanges2.csv", "r")
    rows = csv.reader(resultats)
    for row in rows:
        a = row[1]
    j = -1
    e3 = str(a[j])
    while str(a[j]) != " ":
        j-= 1
        if len(a) >= -j:
            e3 += str(a[j])
        else:
            break
    e3 = float("".join(reversed(e3)))
    resultats.close()
    
    Temps[2][i] = t6-t5
    Argent_echange[2][i] = a3
    Nombre_echange[2][i] = int(e3)
    
    if Nombre_echange[0][i] != Nombre_echange[1][i] or round(Argent_echange[0][i],2) != round(Argent_echange[1][i],2) or round(Argent_echange[0][i],2) != round(Argent_echange[2][i],2) or Nombre_echange[1][i] != Nombre_echange[2][i] or round(Argent_echange[1][i],2) != round(Argent_echange[2][i],2) or Nombre_echange[0][i] != Nombre_echange[2][i]:
        os.rename("Exchanges.csv", "Erreur_Exchanges.csv")
        os.rename("Exchanges2.csv", "Erreur_Exchanges2.csv")
        os.rename("Flow.csv", "Erreur_Flow.csv")
        os.rename("Results.csv", "Erreur_Results.csv")
        os.rename("Dettes.csv", "Erreur_Dettes.csv")
        os.rename("Operations.csv", "Erreur_Operations.csv")
        print ("Nombre échange :", a1, "Argent :", e1)
    
X = [i for i in range(Nombre_essais)]

ax1 = plt.subplot(223)
ax1.plot(X,Temps[0], 'r-.', label = "Heuristique")
ax1.plot(X,Temps[1], 'g:o', label = "Min -> Flow")
ax1.plot(X,Temps[2], 'b d', label = "Flow -> Min")
ax1.set_title("Temps d'execution des différentes méthodes (en secondes)")
ax1.legend()

ax2 = plt.subplot(222)
ax2.plot(X,Argent_echange[0], 'r-.', label = "Heuristique")
ax2.plot(X,Argent_echange[1], 'g:o', label = "Min -> Flow")
ax2.plot(X,Argent_echange[2], 'b d', label = "Flow -> Min")
ax2.set_title("Nombre total d'argent échangé")
ax2.legend()

ax3 = plt.subplot(221)
ax3.plot(X,Nombre_echange[0], 'r-.', label = "Heuristique")
ax3.plot(X,Nombre_echange[1], 'g:o', label = "Min -> Flow")
ax3.plot(X,Nombre_echange[2], 'b d', label = "Flow -> Min")
ax3.set_title("Nombre de transactions")
ax3.legend()

ax4 = plt.subplot(224)
ax4.plot(X,Temps[0], 'r-.', label = "Heuristique")
ax4.plot(X,Temps[2], 'b d', label = "Flow -> Min")
ax4.set_title("Temps d'execution des différentes méthodes (en secondes)")
ax4.legend()

plt.show()

print(Temps)
print(Argent_echange)
print(Nombre_echange)