#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 15:57:03 2021

@author: yohanpellerin
"""
from math import *

def lecturedata(filename):

    data = []
    
    with open(filename) as f:
        keys = [w.strip() for w in next(f).split(';')]
        for line in f:
            l = [w.strip() for w in line.split(';')]
            data.append({k:v for k, v in zip(keys, l)})
    return(data)

class Pile:
    
    def __init__(self):
        self.__liste=[]

    def ajoute(self,l):
        self.__liste.append(l)
        
    def supprime(self):
        v=self.__liste.pop()
        return v
    def __str__(self):
        S=''
        for e in self.__liste:
            S=S + ""+ e['nom'] + " " + e['prenom'] + "/n"
        return S
    def teille(self):
        return len(self.__liste)

class File:
    def __init__(self):
        self.__liste=[]

    def ajoute(self,l):
        self.__liste.append(l)
        
    def supprime(self):
        v=self.__liste.pop(0)
        return v
    def __str__(self):
        S=''
        for e in self.__liste:
            S=S + ""+ e['nom'] + " " + e['prenom'] + "/n"
        return S
    def teille(self):
        return len(self.__liste)
    
    def renvoie(self, critere):
        for v in self.__liste:
            if critere(v)== True  :
                return v
        return False
class Tas:
    def __init__(self):
        self.__liste=[]
    
    def get_racine (self):
        return self.__liste[0]
    def get_fils_gauche(self,i):
        return self.__liste[2*i+1]
    def get_fils_droit(self,i):
        return self.__liste[2*i+2]
    def ajoute(self,l):
        self.__liste.append(l)
        
    def supprime(self):
        v=self.__liste.pop(0)
        return v
    def get_parent(self,i):
        return self.__liste[(i-1)//2]
    
    def inserer(self,a):
        self.ajoute(a)
        t=self.__liste
        i=len(self.__liste)-1
        while self.get_parent(i) > self.__liste [i] and i!=0 :
            
            t[i],t[(i-1)//2]=  t[(i-1)//2],t[i]
            i=(i-1)//2
            

if __name__ == '__main__':  
             
    data= lecturedata("etudiants.txt")
    print(data)
    
    somme = 0
    for d in data:
        somme += int (d["moyenne"])
    print(somme/ len(data))

    p = File()
    for d in data:
        p.ajoute(d)
    f = p.supprime()
    print(f)

    tas = Tas()
    for d in data:
        tas.inserer(int(d['moyenne']))
    r = tas.get_racine()
    fg_i = tas.get_fils_gauche(0)
    ffg_i = tas.get_fils_droit(0)
    print(r, fg_i, ffg_i) # affiche racine, fis gauche et petit-fils gauche
    
