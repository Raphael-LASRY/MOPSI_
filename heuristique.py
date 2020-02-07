# Gestion des matrices

import numpy as np

# Gestion de la résolution en nombre entiers

from test_integer import completer_dettes as dettes

dettes = dettes()
del(dettes[0])

Remboursement = []

dettes = sorted(dettes, key=lambda montant: montant[1])

moy = 0
for dette in dettes:
    moy += dette[1]
moy/=len(dettes)
for dette in dettes:
    dette[1] -= moy

test = True

while test:
    test = False
    remboursement = max(-dettes[0][1],dettes[-1][1])
    dettes[0][1] += remboursement
    dettes[-1][1] -= remboursement
    Remboursement.append([dettes[0][0], dettes[-1][0], round(remboursement,2)])
    for dette in dettes:
        if abs(dette[1])>10**(-5):
            test = True
    dettes = sorted(dettes, key=lambda montant: montant[1])
print(Remboursement)