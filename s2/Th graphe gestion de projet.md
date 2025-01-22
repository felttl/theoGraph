
on marque les noeuds avec des notation du type 12/16/4 (pour l'edge entre 0 et 1)

Flot maximal qu'on peut faire passer = min(16+13,20+4)=24
___
- sol initial : Flot = 0
- chemin 1 : 0-1-3-5
- Flot passant = 13 (min(16,12,20))
	- Flot = Flot + 12 = 12
- chemin 2 : S(13)-B(14)-D(4)-t
	- flot passant = 4
- ---
- chemin 3 : s(9)-b(10)-d(7)-c(8) $\rightarrow$ min = 7
---
chemin 4 : $\varnothing$ 

max possible = flot 1 + chemin 2 et 3 (12+4+7) = 23 < max possible de 24


# méthode de gestion de projet
## algorithme de construction de graphe (voir Elearn) exemple :

1. construction du graphe :
	- cond au plus tot:
		- 3 commence au plus tot 1 jour apres 1 : t3-t1 >=1
		- 4 commence au plus tot 3 jours après la fin de 2 (durée de 2->11)
		t4(t2+11)$\geq$ 3 => t4-t2 $\geq$ 3+11 = 14
		- 5 commence au plus tot 1 jour avant la fin de 2 :
		t5-(t2+11-1(1 jour avant la fin)) $\geq$ 0
		- 6 commence au plus tot 0 jour aprèe le début de 4 : t6-t54 >= 0
		- 6 commence au plus tot après la fin de 5 : t6-(t5+5)>=0 --> t6-t5>=5
		- 3 commence au plus tot 8 jours après le début de (4) :
		t8-t4<=8<==>t4-t8>=-8

2. Le graphe 




- Bellman pour le chemin maximal :


$$L=\begin{pmatrix}
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
-inf & 0 & -inf & 14 & 10 & -inf & 11 \\
-inf & -inf & 0 & -8 & -inf & -inf & 5 \\
-inf & -inf & -inf & 0 & -inf & 0 & 8 \\
-inf & -inf & -inf & -inf & 0 & 5 & 5 \\
-inf & -inf & -inf & -inf & -inf & 0 & 4 \\
-inf & -inf & -inf & -inf & -inf & -inf & 0
\end{pmatrix}$$

solution : 
on prend que 6 lignes car les lignes qui suivent la ligne 4 se répètent indéfiniment et c'est donc inutile 
$$M=\begin{pmatrix}
0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 14 & 10 & 5& 11 \\
0 & 0 & 1 & 14 & 10 & 15 & 22 \\
0 & 0 & 1 & 14 & 10 & 15 & 22 \\
0 & 0 & 1 & 14 & 10 & 15 & 22 \\
0 & 0 & 1 & 14 & 10 & 15 & 22 \\
\end{pmatrix}$$

$\rightarrow$ il nous faut 22 jours pour résoudre le problème

d)
questioninterpretation de 
$L_3(1,4)$ le chemin optimal entre 1 et 4 passant au plus par 3 sommets 

d4) --> c'est Floyd


voyageur passer par tous les sommets (faire un cycle revenir au début et graphe complet)





 