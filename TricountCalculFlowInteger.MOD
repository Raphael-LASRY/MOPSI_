/* Données connues du problème auxquelles on fait référence dans la partie Data */

set Name_Users;
param Debt{Name_Users}; /* Montants avancés par chaque personne */

table tab_Amount IN "CSV" "Dettes.csv" : 
  Name_Users <- [NAME], Debt ~ VALUE;
param Sum_Amount := sum{k in Name_Users}(abs(Debt[k]));

set Nb_Exchanges;
param Nb_{Nb_Exchanges};
table tab_Exchange IN "CSV" "Exchanges.csv":
  Nb_Exchanges <- [EXCHANGES], Nb_ ~ NUMBER;
/* Introduction des paramètres et des variables */

var Exchanges{Name_Users, Name_Users}, binary; /* Matrice indiquant s'il y a eu un échange entre l'individu i et j */
var Flow{Name_Users, Name_Users} >= 0;  /* Matrice indiquant combien l'individu i doit à l'individu j */

/* Corps du problème d'optimisation */

minimize Nb_exchanges : sum{i in Name_Users, j in Name_Users}(Flow[i, j]); /* Minimisation du nombre de transactions */

s.t. Nb_Exchanges_fix {t in Nb_Exchanges} : sum{k in Name_Users, l in Name_Users} Exchanges[k, l] = Nb_[t]; /* Il y a un nombre de transactions fixé */
s.t. Equilibrium{m in Name_Users} : Debt[m] = sum{n in Name_Users}(Flow[m, n] - Flow[n, m]); /* L'équilibre budgetaire doit etre respecté */

solve;

/* Visualisation des résultats */

printf {i in Name_Users, j in Name_Users: Flow[i, j]!=0} "%s,%g,%s \n", j, Flow[i, j], i >> "Results_integer.csv"; /* On affiche uniquement les transactions non nulles entre personnes */

end;

