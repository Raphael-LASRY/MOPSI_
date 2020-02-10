/* Données connues du problème auxquelles on fait référence dans la partie Data */

set Name_User;
set Index_Operation dimen 2;
param Sum_High{Index_Operation}; /* Montants hauts pour chaque personne */
param Sum_Low{Index_Operation}; /* Montants bas pour chaque personne */
param Sum_Real{Index_Operation}; /* Montants réels pour chaque personne */

table noms IN "CSV" "Dettes.csv" :
  Name_User <- [NAME];
table tab_Entier IN "CSV" "Results_fourchettes.csv" : 
  Index_Operation <- [NAMEPAY,NAMEPAYED], Sum_High ~ SUMHIGH, Sum_Low ~ SUMLOW, Sum_Real ~ SUMREAL;

/* Introduction des paramètres et des variables */

var Flow{Index_Operation} >= 0 integer;  /* Matrice indiquant combien l'individu i doit à l'individu j en nombre entier */
var Ecart {Name_User}; /* Ecart pour chaque personne */

/* Corps du problème d'optimisation */

minimize Nombre_ecart : sum{i in Name_User} Ecart[i]; /* Minimisation des earts */

s.t. High{(k, l) in Index_Operation} : Flow[k, l] >= Sum_Low[k, l]; /* La transaction est supérieure à la fouchette basse */
s.t. Low{(m, n) in Index_Operation} : Flow[m, n] <= Sum_High[m, n]; /* La transaction est inférieure à la fouchette haute */
s.t. Abs1 {t in Name_User} : Ecart[t] >= sum{(u, v) in Index_Operation : u == t or v == t} (Flow[u, v] - Sum_Real[u, v]); /* Les ecarts sont les valeurs absolues */
s.t. Abs2 {p in Name_User} : Ecart[p] >= sum{(x, y) in Index_Operation : x == p or y == p} (Sum_Real[x, y] - Flow[x, y]); /* Les ecarts sont les valeurs absolues */

solve;

/* Visualisation des résultats */

printf "\n" >> "Results_integer.csv";
printf {(b, g) in Index_Operation} "%s va effectivement payer %g a %s\n", b, Flow[b, g], g >> "Results_integer.csv"; /* On affiche ce que les gens ont effectivement payé */
printf "\n" >> "Results_integer.csv";
printf {h in Name_User} "L'ecart total pour l'utilisateur %s est de %g\n", h, Ecart[h] >> "Results_integer.csv";
printf "\n" >> "Results_integer.csv";
printf "La somme des ecarts est de %g", Nombre_ecart >> "Results_integer.csv";
end;
