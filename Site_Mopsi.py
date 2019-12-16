import pandas as pd
import os 
import csv

op = pd.read_csv("Operations.csv", header = None, index_col = None, sep=",")

test = True
Noms_utilisateurs = 0
Names = []
while test:
    try:
        op[Noms_utilisateurs][0]
    except:
        test = False
    Noms_utilisateurs += 1
Noms_utilisateurs -= 1
for nom in range (1,Noms_utilisateurs):
    Names.append(op[nom][0])

op = pd.read_csv("Operations.csv", index_col = None, sep=",")

L=[["NAME","VALUE"]]
for name in Names:
    L.append([name,sum(op[name])])
# print(L)
   
    
Ldf = pd.DataFrame(L)
if (os.path.exists("Dettes.csv")):
    os.remove("Dettes.csv")
Ldf.to_csv("Dettes.csv", index=False, header=False, sep=",")

compteur = 0
    
for i in range(5):
    if (os.path.exists("Results.csv")):
        os.remove("Results.csv")
    if (os.path.exists("Exchanges.csv")):
        os.remove("Exchanges.csv")
    if (os.path.exists("Flow.csv")):
        os.remove("Flow.csv")
    if (os.path.exists("Exchanges2.csv")):
        os.remove("Exchanges2.csv")
    os.system("python Generation_aleatoire_csv.py")    
    os.system("glpsol -m TricountCalculMin1.MOD")
    os.system("glpsol -m TricountCalculFlow1.MOD")
    os.system("glpsol -m TricountCalculFlow2.MOD")
    os.system("glpsol -m TricountCalculMin2.MOD")
    r1 = open("Exchanges.csv", "r", newline='')
    a = csv.reader(r1)
    A = []
    for row in a:
        A.append(row)
    r2 = open("Exchanges2.csv", "r", newline='')
    b = csv.reader(r2)
    B = []
    for row in b:
        B.append(row)
    if (A[-1]!=B[-1]):
        compteur += 1
    r1.close()
    r2.close()
if (compteur != 0):
    print ("Sur {} calculs il y a eu un écart".format(compteur))
else:
    print("Les deux méthodes donnent le même nombre de transactions")
# os.system("glpsol -m TricountCalculMinInteger.MOD")
# os.system("glpsol -m TricountCalculFlowInteger.MOD")
