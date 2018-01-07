
# Méthodes numériques déterministes

## Projet 4 : Interpolations

Deux méthodes d'interpolation sont étudiées dans ce projet :

 - l'interpolation Lagrangienne calculée en utilisant les polynômes de Lagrange et la base de Newton (interpolation Newtonienne)
 - l'interpolation polynomiale par morceaux avec des splines

Le langage Python 3 a été utilisé pour coder les différentes méthodes. Les
bibliothèques utilisées sont principalement `numpy` et `matplotlib` ; certaines partie du code nécessitent `scipy` et `pylab`. Le rapport à été rédigé avec LaTeX.

Le projet est constitué des fichiers suivants:

 - `newton.py`: contient le code pour l'interpolation lagrangienne et newtonienne
 - `splines.py`: contient le code pour l'interpolation par splines
 - `rapport/` : contient les fichiers `tex` du rapport

### Compilation du rapport

En se plaçant dans le répertoire `rapport/`, ce dernier peut être compilé avec la commande suivante (distribution MikTeX).
``` 
pdflatex main
```

Une version pré-compilée du rapport est disponible à la racine du projet.

### Fichier `newton.py`

Ce fichier contient une classe  `Interpolation` qui permet de calculer le polynôme d'interpolation de Lagrange. Le polynôme est calculé de manière itérative en utilisant la base de Newton. Alternativement, on peut déclencher le calcul du polynôme en utilisant la base de Lagrange grâce à la méthode `Interpolation.lagrange()`. 
La classe `numpy.polynomial.Polynomial` est utilisée pour représenter les polynômes.

``` 
## Exemple d’utilisation du code Python
a = Interpolation(f) # On construit un objet permettant d’interpoler la fonction f
# On ajoute trois points d’ interpolations
a.addPoint(-1)
a.addPoint(0)
a.addPoint(1)
a.P(0) # On évalue le polynôme d’interpolation en 0
a.x(1) # On récupère le deuxième point d’interpolation, ici 0
a.lagrange() # Renvoie le polynôme calculé en utilisant la base de Lagrange
```


Le fichier définit 3 fonctions : 

- `interf()` : interpolation de la fonction $f(x) = 1 / (1+x^2)$
- `interg()` : interpolation de la fonction $g(x) = 2 (1 + \tanh(x)) - x / 10$
- `algocomp()` : comparaison des algorithmes de Lagrange et Newton pour calculer le polynôme d'interpolation.

Le fichier peut également être exécuté sous forme de script :
``` 
python newton.py interf True
```
Description : Interpole la fonction $f$ en utilisant les points de Tchebychev.
``` 
python newton.py interg 15 False
```
Description : Interpole la fonction $g$ en 15 points uniformément répartis.
``` 
python newton.py algocompo
```
Description : Lance l'algorithme de comparaison.


### Fichier `splines.py`

Le fichier contient la définition d'une classe  `Spline` qui permet de calculer l'interpolation polynomiale par morceaux par splines.

Exemple d'utilisation:

``` 
s = Spline(f) # Construction de l'objet Spline pour interpoler f
s.equidistant(10,-6,6) # Ajout de 10 points d'interpolation sur [-6, 6]
s.interpol() # Calcul des splines
err = s.draw(np.linspace(-6,6,200)) # Affichage du graphe et calcul de l'erreur en norme infinie
```

Utilisation sous forme de script :
``` 
python splines.py
```
Description : Calcule les splines pour différentes valeur de pas et affiche les graphes correspondants. Le dernier graphe affiché est un graphe de l'erreur en fonction du pas. La fonction étudiée est $f(x) = \arctan(x^3)$.

# Documentation de `splines.py`

Paramètres pour faire tourner le script :

- Définir de la fonction à interpoler (`f1`)
- Lister avec quels nombre de points d'interpolation les différentes splines vont être crées (`nbList`)
- Modifier le niveau de définition des courbes (dernier paramètre de la fonction `linspace` l.119)

Remarques :

 - Les erreurs et les graphes sont donnés dans l'ordre où les différents nombres de points sont donnés
 -  Le vecteur `err` garde en mémoire les erreurs pour chaque essai



Fonctionnement de la classe Spline:

- Le constructeur de la classe se fait uniquement avec la fonction à interpoler en argument
- Avant toutes autres étapes de calcul, il faut donner à la spline des points d'interpolations.
Pour cela, il y a les méthodes `tchebychev` , `equidistant`, `addPoint`, `addPoints`. Toutes ces méthodes font appel à `addPoint` qui est la méthode "de base"
Le seul moyen de supprimer des points d'interpolation est de recréer la spline.
- La méthode `interpol` calcul les polynômes sur chacun des intervalles de subdivision.
Cette méthode fait appel à la méthode `solveMi` qui détermine uniquement les termes Mi à l'aide d'un système matriciel comme écrit dans le rapport
- La méthode `calcul` retourne la valeur de la spline au point donné en argument
- La fonction `draw` trace la fonction à interpoler et sa spline naturelle sur les points donnés en argument et retourne l'erreur en norme infinie sur ces points



Déclaration des attributs:

- `f` : la fonctionà interpoler, déterminée par le constructeur et non modifiable
- `points` : liste de réels (distincts), peut être rallongées par les méthodes `tchebychev,equidistant`, `addPoint`, `addPoints` mais ne peut-être raccourcie
- `splines` : liste de polynômes, générée par la méthode `interpol`
- `n` : nombre de points d'interpolation, mis à jour à chaque appel de `AddPoint`

Déclaration des fonctions:

- Le constructeur prend en argument une fonction et retourne une spline
- Les méthodes `tchebychev` et `equidistant` prennent en arguments : un nombre de point, le début de l'intervalle,la fin et ne retournent rien
- La méthode `addPoint` prend en argument un réel
- La méthode `addPoints` prend en argument une liste de réels
- La méthode `solveMi` ne prend pas d'argument et retourne la liste des coefficients Mi
- La méthode `interpol` ne prend pas d'argument et ne retourne rien
- La méthode `calcul` prend en argument un réel et retourne un autre réel
- La méthode `draw` rend en argument une liste de points et retourne un réel (positif)

Remarques:
- Pour les méthodes `calcule` et `draw`, il est préférable que le(s) point(s) donné en argument soi(en)t dans l'intervalle défini par les points de la subdivision sans quoi les résultats n'auront pas de sens.
