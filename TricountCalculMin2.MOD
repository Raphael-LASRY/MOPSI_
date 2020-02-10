/* Données connues du problème auxquelles on fait référence dans la partie Data */

set Name_Users;
param Debt{Name_Users}; /* Montants avancés par chaque personne */

table tab_Amount IN "CSV" "Dettes.csv" : 
  Name_Users <- [NAME], Debt ~ VALUE;
param Sum_Amount := sum{k in Name_Users}(abs(Debt[k]));

set Nb_cash_exchange;
param Nb_{Nb_cash_exchange};
table tab_Exchange IN "CSV" "Flow.csv":
  Nb_cash_exchange <- [FLOW], Nb_ ~ NUMBER;

/* Introduction des paramètres et des variables */

var Exchanges{Name_Users, Name_Users}, binary; /* Matrice indiquant s'il y a eu un échange entre l'individu i et j */
var Flow{Name_Users, Name_Users} >= 0;  /* Matrice indiquant combien l'individu i doit à l'individu j */

/* Corps du problème d'optimisation */

minimize Nb_exchanges : sum{i in Name_Users, j in Name_Users}(Exchanges[i, j]); /* Minimisation du nombre de transactions */

s.t. Transaction{k in Name_Users, l in Name_Users} : Exchanges[k, l] >= Flow[k, l]/ (1 + Sum_Amount); /* Il y a transaction si le flow entre i et j est posistif */
s.t. Equilibrium{m in Name_Users} : Debt[m] = sum{n in Name_Users}(Flow[m, n] - Flow[n, m]); /* L'équilibre budgetaire doit etre respecté */
s.t. Cash_exchanges{t in Nb_cash_exchange} : sum{i in Name_Users, j in Name_Users}(Flow[i, j]) = Nb_[t]; /* La somme des echanges est imposée */

solve;

/* Visualisation des résultats */

printf "EXCHANGES,NUMBER\n" >> "Exchanges2.csv";
printf "Number,%d\n",Nb_exchanges >> "Exchanges2.csv";

printf {i in Name_Users, j in Name_Users: Flow[i, j]!=0} "%s doit %.2f à %s \n", j, Flow[i, j], i >> "Results.csv"; /* On affiche uniquement les transactions non nulles entre personnes */
printf "La somme totale des échanges est de %.2f", sum{o in Name_Users, b in Name_Users} Flow[o, b] >> "Results.csv";

end;
