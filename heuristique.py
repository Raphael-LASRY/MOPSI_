# Gestion des matrices

import numpy as np

# Gestion de la résolution en nombre entiers

from test_integer import completer_dettes as dettes

def calcul_heuristique(R):
    Dettes = dettes()
    del(Dettes[0])
    
    Remboursement = []
    
    Dettes = sorted(Dettes, key=lambda montant: montant[1])
    
    moy = 0
    for dette in Dettes:
        moy += dette[1]
    moy/=len(Dettes)
    for dette in Dettes:
        dette[1] -= moy
    
    test = True
    
    while test:
        test = False
        remboursement = min(-Dettes[0][1],Dettes[-1][1])
        Dettes[0][1] += remboursement
        Dettes[-1][1] -= remboursement
        Remboursement.append([Dettes[0][0], Dettes[-1][0], round(remboursement,2)])
        for dette in Dettes:
            if abs(dette[1])>10**(-5):
                test = True
        Dettes = sorted(Dettes, key=lambda montant: montant[1])
    
    #R.append([("Il y a ", len(Remboursement), " échanges")])
    Argent_echange = 0
    for remboursement in Remboursement:
        R.append((remboursement[0] + " doit " + str(remboursement[2]) + " à " + remboursement[1]))
        Argent_echange += remboursement[2]
    R.append(("La somme totale échangée est de " + str(Argent_echange)))