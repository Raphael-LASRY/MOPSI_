/* Données connues du problème auxquelles on fait référence dans la partie Data */

set Name_Users;
param Debt{Name_Users}; /* Montants avancés par chaque personne */

table tab_Amount IN "CSV" "C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/Dettes.csv" : 
  Name_Users <- [NAME], Debt ~ VALUE;
param Sum_Amount := sum{k in Name_Users}(abs(Debt[k]));


/* Introduction des paramètres et des variables */

var Flow{Name_Users, Name_Users} >= 0;  /* Matrice indiquant combien l'individu i doit à l'individu j */

/* Corps du problème d'optimisation */

minimize Cash_exchanges : sum{i in Name_Users, j in Name_Users}(Flow[i, j]); /* Minimisation du nombre de cash échangé */

s.t. Equilibrium{m in Name_Users} : Debt[m] = sum{n in Name_Users}(Flow[m, n] - Flow[n, m]); /* L'équilibre budgetaire doit etre respecté */

solve;

/* Visualisation des résultats */

printf "FLOW,NUMBER\n" >> "C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/Flow.csv";
printf "Number,%g\n",Cash_exchanges >> "C:/Users/pc/Desktop/Enpc/2A/MOPSI/MOPSI/MOPSI/Flow.csv";

end;
