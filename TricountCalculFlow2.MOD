/* Donn�es connues du probl�me auxquelles on fait r�f�rence dans la partie Data */

set Name_Users;
param Debt{Name_Users}; /* Montants avanc�s par chaque personne */

table tab_Amount IN "CSV" "Dettes.csv" : 
  Name_Users <- [NAME], Debt ~ VALUE;
param Sum_Amount := sum{k in Name_Users}(abs(Debt[k]));


/* Introduction des param�tres et des variables */

var Flow{Name_Users, Name_Users} >= 0;  /* Matrice indiquant combien l'individu i doit � l'individu j */

/* Corps du probl�me d'optimisation */

minimize Cash_exchanges : sum{i in Name_Users, j in Name_Users}(Flow[i, j]); /* Minimisation du nombre de cash �chang� */

s.t. Equilibrium{m in Name_Users} : Debt[m] = sum{n in Name_Users}(Flow[m, n] - Flow[n, m]); /* L'�quilibre budgetaire doit etre respect� */

solve;

/* Visualisation des r�sultats */

printf "FLOW,NUMBER\n" >> "Flow.csv";
printf "Number,%g\n",Cash_exchanges >> "Flow.csv";

end;