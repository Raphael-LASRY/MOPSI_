import pandas as pd
import os 

op = pd.read_csv("C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/Operations.csv", header = None, index_col = None, sep=",")

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

op = pd.read_csv("C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/Operations.csv", index_col = None, sep=",")

L=[["NAME","VALUE"]]
for name in Names:
    L.append([name,sum(op[name])])
print(L)
   
    
Ldf = pd.DataFrame(L)
Ldf.to_csv("C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/Dettes.csv", index=False, header=False, sep=",")

if (os.path.exists("C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/Results.csv")):
    os.remove("C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/Results.csv")
if (os.path.exists("C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/Exchanges.csv")):
    os.remove("C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/Exchanges.csv")
    
os.system("glpsol -m C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/TricountCalculMin1.MOD")
os.system("glpsol -m C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/TricountCalculFlow1.MOD")
