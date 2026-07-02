# Example: Mathematical / Algorithm Explanation (Sorting)

**User**: Explique-moi le fonctionnement de l'algorithme Quicksort en détail.

**Agent response**:
### ⚡ Algorithme de Tri Rapide (Quicksort)

L'algorithme **Quicksort** est basé sur le paradigme "Diviser pour régner" (Divide and Conquer).

#### 1. Le principe du pivot
L'idée est de choisir un élément dans le tableau (appelé **pivot**) et de réorganiser les autres éléments :
* Tous les éléments **inférieurs** au pivot sont déplacés à sa gauche.
* Tous les éléments **supérieurs** au pivot sont déplacés à sa droite.

Une fois cette étape (le *partitionnement*) terminée, le pivot est à sa place définitive.

```
Tableau initial:  [5, 2, 9, 3, 7, 6, 1]  (Pivot choisi = 5)
Après partition:  [2, 3, 1] < 5 < [9, 7, 6]
Recurrence:       Quicksort(gauche) + [5] + Quicksort(droite)
```

#### 2. Complexité Temporelle
* **Dans le meilleur des cas (partition équilibrée)** : $\mathcal{O}(N \log N)$
* **Dans le pire des cas (tableau déjà trié et mauvais choix de pivot)** : $\mathcal{O}(N^2)$
