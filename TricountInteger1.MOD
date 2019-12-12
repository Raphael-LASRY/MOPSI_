/* Données connues du problème auxquelles on fait référence dans la partie Data */

set Name;
param Sum_High{Name}; /* Montants hauts pour chaque personne */
param Sum_Low{Name}; /* Montants bas pour chaque personne */

table tab_Entier IN "CSV" "Results_integer.csv" : 
  Name <- [NAMEPAY], Sum_High ~ SUMHIGH, Sum_Low ~ SUMLOW, Sum_Real ~ SUMREAL;

/* Introduction des paramètres et des variables */

var Flow{Name} >= 0;  /* Matrice indiquant combien l'individu i doit à l'individu j */
var Ecart {Name}; /* Ecart pour chaque personne */

/* Corps du problème d'optimisation */

minimize Nombre_ecart {i in Name} : Ecart[i]; /* Minimisation du nombre de transactions */

s.t. High{k in Name} : Flow[k] >= Sum_Low[m]; /* La transaction est supérieure à la fouchette basse */
s.t. Low{m in Name} : Flow[m] <= Sum_High[m]; /* La transaction est inférieure à la fouchette haute */
s.t. Abs1 {l in Name} Ecart[l] >= sum{t in Operation : Name_Operation = l} (Flow[t] - Sum_Real[t]); /* Les ecarts sont les valeurs absolues */
s.t. Abs2 {p in Name} Ecart[p] >= sum{v in Operation : Name_Operation = p} (Flow[v] - Sum_Real[v]); /* Les ecarts sont les valeurs absolues */

solve;

/* Visualisation des résultats */

printf {j in Name} "%s va effectivement payer %g \n", j, Flow[j] >> "Results_integer.csv" /* On affiche ce que les gens ont effectivement payé */

end;
