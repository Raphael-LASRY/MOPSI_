import csv
import random as rd
import numpy as np

Nombre_utilisateurs = rd.randint(3,7)
Nombre_operations = rd.randint(1,5)

Matrice_operations = np.empty((Nombre_operations, Nombre_utilisateurs-1))
r = open("Operations.csv", "w")
r.write("Index,")
for i in range(1, Nombre_utilisateurs):
    r.write("Name" + str(i) + ",")    
r.write("Name" + str(Nombre_utilisateurs))
r.write("\n")

for i in range(Nombre_operations):
    for j in range(Nombre_utilisateurs-1):
        Matrice_operations[i, j] = 20*rd.random() # On paie entre 0 et 20€
print(Matrice_operations)
for i in range(Nombre_operations):
    Matrice_operations[i] -= np.mean(Matrice_operations[i, :])
print(Matrice_operations)

delta=np.zeros(Nombre_operations)
for i in range(Nombre_operations):
    for j in range(Nombre_utilisateurs-1):
        delta[i] -= round(Matrice_operations[i, j],2)
        
for i in range(Nombre_operations):
    r.write(str(i)+",")
    for j in range(Nombre_utilisateurs-1):
        r.write(str(round(Matrice_operations[i, j],2)))
        r.write(",")
    r.write(str(round(delta[i],2)))
    r.write("\n")