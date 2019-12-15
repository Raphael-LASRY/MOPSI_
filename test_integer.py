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
print(L)

    
Ldf = pd.DataFrame(L)
if (os.path.exists("Dettes.csv")):
    os.remove("Dettes.csv")
Ldf.to_csv("Dettes.csv", index=False, header=False, sep=",")

if (os.path.exists("Results.csv")):
    os.remove("Results.csv")
if (os.path.exists("Exchanges.csv")):
    os.remove("Exchanges.csv")

#Integer
if (os.path.exists("Results_integer.csv")):
    os.remove("Results_integer.csv")
r = open("Results_integer.csv", "a")
r.write("NAMEPAY,SUM,NAMEPAYED \n")
r.close()



# Calcul exact solutions
os.system("glpsol -m TricountCalculMin1.MOD")
os.system("glpsol -m TricountCalculFlowInteger.MOD")
# 
# 
# Dettes = [ [name,0,0] for name in Names] # Le premier 0 = la fourchette qui l'arrange pas, le 2e = la fourchette qui l'arrange
# r = open("Results_integer.csv", "r")
# test = csv.reader(r)
# 
# for row in test:
#     for perso in Dettes:
#         if perso[0] == row[0]:
#             perso[1] += int(float(row[1][:]))
#             perso[2] += int(float(row[1][:])) + 1
#         elif perso[0] == row[2]:
#             perso[1] += -int(float(row[1][:])) -1
#             perso[2] += -int(float(row[1][:]))
#             
# print("###########################################")
# print(Dettes)
# print("###########################################")
# 
# Dettesdf = pd.DataFrame(Dettes)
# if (os.path.exists("Dettes_fourchettes.csv")):
#     os.remove("Dettes_fourchettes.csv")
# Dettesdf.to_csv("Dettes_fourchettes.csv", index=False, header=False, sep=",")
# r.close()




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



