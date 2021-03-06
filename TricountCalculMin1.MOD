/* Introduction des tables et param�tres */

set Name_Users;
param Debt{Name_Users}; /* Montants avanc�s par chaque personne */

table tab_Amount IN "CSV" "Dettes.csv" : 
  Name_Users <- [NAME], Debt ~ VALUE;
param Sum_Amount := sum{k in Name_Users}(abs(Debt[k]));

/* Introduction des variables */

var Exchanges{Name_Users, Name_Users}, binary; /* Matrice indiquant s'il y a eu un �change entre l'individu i et j */
var Flow{Name_Users, Name_Users} >= 0;  /* Matrice indiquant combien l'individu i doit � l'individu j */

/* Corps du probl�me d'optimisation */

minimize Nb_exchanges : sum{i in Name_Users, j in Name_Users}(Exchanges[i, j]); /* Minimisation du nombre de transactions */

s.t. Transaction{k in Name_Users, l in Name_Users} : Exchanges[k, l] >= Flow[k, l]/ (1 + Sum_Amount); /* Il y a transaction si le flow entre i et j est posistif */
s.t. Equilibrium{m in Name_Users} : Debt[m] = sum{n in Name_Users}(Flow[m, n] - Flow[n, m]); /* L'�quilibre budgetaire doit etre respect� */

solve;

/* Visualisation des r�sultats */

printf "EXCHANGES,NUMBER\n" >> "Exchanges.csv";
printf "Number,%d\n",Nb_exchanges >> "Exchanges.csv";

end;
