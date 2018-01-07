# -*- coding: utf-8 -*-
"""
Wantz Julien
Chambrin Vincent

Sujet 4, Partie II
Interpolation polynomiale par morceu : splines
"""

import numpy as  np   
import scipy as sp
from pylab import *
import matplotlib.pyplot as plt
import numpy.polynomial as poly


class Spline:
    def __init__(self,f):
        self.points = [] #Les points d'interpolations
        self.f = f #La fonction à interpoler
        self.splines = [] #La liste des polynômes d'interpolation sur chaque subdivision
        self.n = 0 #Le nombre de points d'interpolations
        
    #Retourne le i-ième point d'interpolation
    def x(self,i):
        return self.points[i]
    
    #Construit les points d'interpolation de Tchebychev sur l'intervalle ]start,stop[
    def tchebychev(self,_n,start,end):
        self.n = _n
        for i in np.arange(1,_n+1):
            self.points.append((start+end)/2.0 + (end-start)*0.5*np.cos((2*i-1)*np.pi/(2*_n)))
            
    #Construit n points d'interpolations équidistants sur l'intervalle [start,stop]
    def equidistant(self,_n,start,end):
        self.n = _n
        for i in range(_n):
            self.points.append(start+i*(end-start)/(_n-1))
            
    #Rajoute le points rentré en argument à condition qu'il ne soit pas déjà dans la liste
    def addPoint(self,x):
        if len(self.points) == 0 :
            self.points.append(x)
        else :
            for i in range(len(self.points)):
                if x < self.points(i):
                    self.points.insert(i,x)
                    break
                elif x == self.points(i):
                    break
            if i == len(self.points) - 1 and x != self.points(i):
                self.points.append(x)
            
    #Calcul des coefficients Mi = s"(xi)
    def solveMi(self):
        A = np.zeros((self.n-2,self.n-2))
        B = np.zeros((self.n-2))
        for i in np.arange(1,self.n-1):
            A[i-1,i-1] = 2/3
            hi1 = self.x(i)-self.x(i-1)
            hi2 = self.x(i+1)-self.x(i)
            if i > 1:
                A[i-1,i-2] = (1/3)*hi1/(hi1+hi2)
            if i < self.n-2:
                A[i-1,i] = (1/3)*hi2/(hi1+hi2)
            B[i-1] = (2/(hi1+hi2))*( (self.f(self.x(i+1))-self.f(self.x(i)))/hi2 - (self.f(self.x(i))-self.f(self.x(i-1)))/hi1 )
        M = np.linalg.solve(A,B)
        M = np.concatenate(([0],M,[0]))
        return M
    
    #Crée les différents polynomes sur les intervalles [xi,xi+1]
    def interpol(self):
        M = self.solveMi()
        for i in range(self.n-1):
            P1 = poly.Polynomial([(-1)*self.points[i],1])
            P2 = poly.Polynomial([self.points[i+1],-1])
            P = P2*(self.f(self.points[i])/(self.points[i+1]-self.points[i]) - (self.points[i+1] - self.points[i])*M[i]/6)
            P += P2*P2*P2*M[i]/(6*(self.points[i+1]-self.points[i]))
            P += P1*(self.f(self.points[i+1])/(self.points[i+1]-self.points[i]) - (self.points[i+1] - self.points[i])*M[i+1]/6)
            P += P1*P1*P1*M[i+1]/(6*(self.points[i+1]-self.points[i]))
            self.splines.append(P)
            
    #Calcul la valeur de la spline au point rentré en argument
    def calcul(self,x):
        i = 0
        y = 0
        while i != self.n and x > self.points[i]:
            i += 1
        if i > 0 and i < self.n:
            y = self.splines[i-1](x)
        if i == 0 and x == self.points[0]:
            y = self.splines[0](x)
        return y
    
    #Trace la fonction à interpoler et sa spline naturelle aux points de la liste X et retourne l'erreur en norme L2
    def draw(self,X):
        plt.figure()
        Y = []
        for x in X:
            Y.append(self.calcul(x))
        plt.plot(X,Y,label = 'spline')
        plt.plot(X,self.f(X), label = 'f')
        plt.legend()
        err = (self.f(X)-Y)
        return np.max(np.abs(err))
        

#Définition de la fonction que nous voulons interpoler
def f1(x):
    return np.arctan(x**3)

def f2(x):
    return +0.2*x**2 + 3*x + 4

err = []
nbList = [5,10,15,30,90]
nbList.reverse()
for nb in nbList:
    s = Spline(f1)
    s.equidistant(nb,-6,6)
    s.interpol()
    err.append(s.draw(np.linspace(-6,6,200)))
    print('L erreur pour ',nb,' points d interpolation est ',err[-1])
    
figure()
H = [1/(x-1) for x in nbList]
plt.plot(H,err)
plt.show()
