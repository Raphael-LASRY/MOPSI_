import pandas as pd
import os 

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
    
#os.system("glpsol -m TricountCalculMin1.MOD")
#os.system("glpsol -m TricountCalculFlow1.MOD")
os.system("glpsol -m TricountCalculMinInteger.MOD")
os.system("glpsol -m TricountCalculFlowInteger.MOD")
