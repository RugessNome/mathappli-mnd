
import numpy as np
from numpy.polynomial import Polynomial

## Calcul du polynôme d'interpolation
    
class Interpolation:
    def __init__(self, f):
        self.points = [] # la liste des points d'interpolation
        self.f = f # la fonction a interpoler
        self.P = Polynomial([0]) # le polynôme d'interpolation
        # contient les résultats des calculs de différences divisées
        self.cache = dict() 
        
    # Renvoie le point d'interpolation d'indice i
    def x(self, i):
        return self.points[i]
        
    # Renvoie le polynôme de la base Tchebychev associé au point d'interpolation 
    # d'indice i
    def Li(self, i):
        P = Polynomial([1])
        for j in range(len(self.points)):
            if j == i:
                continue
            P = P * Polynomial([-self.x(j), 1]) / (self.x(i) - self.x(j))
        return P
        
    # Renvoie le polynôme d'interpolation calculé à partir de la base de 
    # Lagrange
    def lagrange(self):
        L = Polynomial([0])
        for j in range(0, len(self.points)):
            L += self.Li(j) * self.f(self.x(j)) 
        return L
        
    # Calcul la différence divisée associée aux points d'indice i à j
    def diffdiv(self, i, j):
        if i == j:
            return self.f(self.x(i))
        c = self.cache.get((i,j)) # On regarde si le résultat est dans le cache
        if c != None:
            return c
        val = self.diffdiv(i+1, j) - self.diffdiv(i, j-1)
        val = val / (self.x(j) - self.x(i))
        self.cache[(i,j)] = val # On écrit le résultat dans le cache
        return val
      
    # Renvoie le polynôme de la base de Newton associée à la différence divisée 
    # d'ordre n
    # Cette fonction est utilisée pour calculer le polynôme d'interpolation de 
    # degré n à partir de celui de degré n-1
    def newton(self, n):
        e = Polynomial([1])
        X = Polynomial([0, 1])
        for i in range(n):
            e = e * (X - self.x(i))
        return e
    
    # Ajoute un point d'interpolation et renvoie le nouveau polynôme 
    # d'interpolation calculé avec les différences divisées
    def addPoint(self, x):
        self.points.append(x)
        self.P = self.P + self.diffdiv(0, len(self.points)-1) * self.newton(len(self.points) - 1)
        return self.P
        
    # Ajoute les points d'interpolation à partir de la liste pts
    # La fonction appelle addPoint() pour chaque point de la liste
    def addPoints(self, pts):
        for p in pts:
            self.addPoint(p)
      
    # Renvoie les n points de Tchebychev pour une interpolation dans [a, b]
    def tchebychev(self, n, a = -1, b = 1):
        pts = []
        for k in range(1, n+1):
            pts.append(np.cos((2*k-1)/(2*n) * np.pi))
        return (a+b) / 2 + (b-a) / 2 * np.array(pts)
        
    # Renvoie n points uniformément répartis dans [a, b]
    def uniform(self, n, a = -1, b = 1):
        if n == 1:
            return (a+b) / 2
        pts = []
        for i in range(0, n):
            pts.append(a + i * (b-a) / (n-1))
        return pts


## Interpoltion de la fonction f
from matplotlib.pyplot import *
close("all") # Ferme toute les fenêtres graphiques

def f(t):
    return 1 / (1+t**2)

def interf(ptsTcheby = False):
    clf()
    xmin = -5
    xmax = 5
    samples = np.arange(xmin, xmax+0.05, 0.05)
    plot(samples, f(samples), label='$f$')
    for i in [3, 9, 17]:
        a = Interpolation(f)
        if ptsTcheby:
            a.addPoints(a.tchebychev(i, xmin, xmax))
        else:
            a.addPoints(a.uniform(i, xmin, xmax))
        plot(samples, a.P(samples), label='$p_{' + str(i-1) + '}$')
        print('Norme infinie (f - p_' + str(i-1) + ') : ', max(np.abs(f(samples)-a.P(samples))))
    
    axis([-5.5, 5.5, -0.5, 1.5]) # les axes : [xmin, xmax, ymin, ymax]
    xlabel("x")
    #title("Interpolation polynomiale de $f$ (points équidistants)")
    legend() # Affiche la légende
    show()

    
## Interpolation de la fonction g
def g(x):
    return 2 * (1 + np.tanh(x)) - x / 10

def interg(nbPoint = 9, ptsTcheby = False):
    figure() # Nouvelle figure
    clf()
    xmin = -6
    xmax = 6
    samples = np.arange(xmin, xmax+0.05, 0.05)
    plot(samples, g(samples), label='$g$')
    a = Interpolation(g)
    if ptsTcheby:
        a.addPoints(a.tchebychev(nbPoint, xmin, xmax))
    else:
        a.addPoints(a.uniform(nbPoint, xmin, xmax))
    plot(samples, a.P(samples), label='$p_{' + str(nbPoint-1) + '}$')
    axis([-6.5, 6.5, -1, 5])
    xlabel("x")
    legend()
    show()

    ## On peut évaluer l'intégrale de g à partir des polynômes interpolateurs
    print("Evaluation de l'intégrale de g :")
    import scipy.integrate as integrate
    i1 = integrate.quad(g, xmin, xmax)
    P = a.P.integ()
    i2 = P(xmax) - P(xmin)
    print("Scipy : ", i1, ", Polynome d'interpolation : ", i2)


## Comparaison des algorithmes
def algocomp():
    import time
    import random
    import math
    print("Comparaison des algorithmes de Newton et Lagrange")
    print("Principe : on génère un nombre croissant de points dans [-1, 1]")
    print("On mesure le temps en seconde nécessaire pour calculer le polynôme d'interpolation de cos() en ces points.")
    for nbPoints in [10, 20, 30, 40, 50, 60, 70, 80]:
        a = Interpolation(math.cos)
        start = time.time()
        for n in range(nbPoints):
            a.addPoint((2*random.random()-1))
        end = time.time()
        print("Newton {} pts : {}s".format(nbPoints, end-start))
        start = time.time()
        a.lagrange()
        end = time.time()
        print("Lagrange {} pts : {}s".format(nbPoints, end-start))
    

# Execution sous forme de script
if __name__ == "__main__":
    import sys
    argc = len(sys.argv)
    if argc > 1:
        procedure = sys.argv[1]
        if procedure == 'algocomp':
            algocomp()
        elif procedure == 'interg':
            if argc == 3:
                interg(int(sys.argv[2]))
            elif argc == 4:
                interg(int(sys.argv[2]), sys.argv[3] == 'True' or sys.argv[3] == 'true')
            else:
                interg()
        elif procedure == 'interf':
            if argc == 3:
                interf(sys.argv[2] == 'True' or sys.argv[2] == 'true')
            else:
                interf()
        else:
            print('Unknown procedure')

