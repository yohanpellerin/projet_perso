#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 19:50:19 2021

@author: yohanpellerin
"""

import time
from PIL import Image # importation de la librairie d’image PILLOW
import numpy as np
import matplotlib.pyplot as plt
from math import * # fonctions essentielles de la librairie math im = Image.open("lyon.png") # ouverture du fichier d’image


    
def peindre(px, x, y, w, h, couleur):
    for i in range(w):
        for j in range(h):
            px[x+i, y+j] = couleur

def moyenne(px, x, y, w, h):
    sr, sg, sb = 0, 0, 0
    for i in range(w):
        for j in range(h):
            r, g, b = px[x+i, y+j][0:3]
            sr += r
            sg += g
            sb += b
    n = w * h
    return sr/n, sg/n, sb/n

    
def ecart_type(px, x, y, w, h):
    sr, sg, sb = 0, 0, 0
    sqr, sqg, sqb = 0, 0, 0
    for i in range(w):
        for j in range(h):
            r, g, b = px[x+i, y+j][0:3]
            sr += r
            sg += g
            sb += b
            sqr += r*r
            sqg += g*g
            sqb += b*b
    n = w * h
    return sqrt(sqr/n - (sr/n)**2), sqrt(sqg/n - (sg/n)**2), sqrt(sqb/n - (sb/n)**2)

    # -----------------------------------------------------------------------------------#
    #   modification de l'ecart type pour mettre en avant le vert                        #
    # on reprend la même structure on modifie juste la sortie en la ponderant            #
    # les coefficient de pondération sont ici (1,5/3,1/3)                                #                               
    #------------------------------------------------------------------------------------#

def ecart_type_pondérer(px, x, y, w, h):
    sr, sg, sb = 0, 0, 0
    sqr, sqg, sqb = 0, 0, 0
    for i in range(w):
        for j in range(h):
            r, g, b = px[x+i, y+j][0:3]
            sr += r
            sg += g
            sb += b
            sqr += r*r
            sqg += g*g
            sqb += b*b
    n = w * h
    return sqrt(sqr/n - (sr/n)**2), (5/3)*sqrt(sqg/n - (sg/n)**2), (1/3)*sqrt(sqb/n - (sb/n)**2)

def homogeneite(px,x, y, w, h, seuil):
    ect      = ecart_type(px,x, y, w, h)
    moy_ect  = (ect[0]+ect[1]+ect[2])/3
    homogene = moy_ect <= seuil
    return homogene

    # -----------------------------------------------------------------------------------#
    #   nouvelle fonction homogéneité  (expliqué dans le rapport                         #                             
    #------------------------------------------------------------------------------------#
def homogeneite_modifie(px,x,y,w,h,x0,y0,seuil):
    r=min((x-x0)**2,(x+w-x0)**2)+min((y-y0)**2,(y+h-y0)**2)
    nouveau_seuil = seuil*(r/4000000+1)
    if sum(ecart_type_pondérer(px,x, y, w, h))/3< nouveau_seuil:
        return(True)
    else: 
        False       
        
def partition(x,y,w,h):
    assert w>0 and h> 0 and not w==h==1
    i = (w+1)//2
    j = (h+1)//2
    a = (x,y,i,j)
    if w>1:
        b = (x+i,y,w-i,j)
    else: b = None
    if h>1:
        c = (x,y+j,i,h-j)
    else: c = None
    if w>1 and h>1:
        d = (x+i,y+j,w-i,h-j)
    else: d = None
    return(a,b,c,d)
    # ------------------------------------------------------------------#
    #   nouvelle classe noeud                                           #
    #on a simplement retirer les attributs donnant les fils d'un noeud  #               
    #-------------------------------------------------------------------#

class Noeud:
    def __init__(self, x, y, l, h, r, v, b):
            self.x = x
            self.y = y
            self.l = l
            self.h = h
            self.r = r
            self.v = v
            self.b = b
            
   
def compter(n):
    if n==None:
        return 0
    else:
        return 1 + compter(n.bd) + compter(n.bg) + compter(n.hg) + compter(n.hd)
    
    # ------------------------------------------------------------------#
    #    classe noeud initiale                                          #
    #-------------------------------------------------------------------#
class Noeud1:
    def __init__(self, x, y, l, h, r, v, b, hg, hd, bg, bd):
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.r = r
        self.v = v
        self.b = b
        self.hg = hg # haut-gauche
        self.hd = hd # haut-droite
        self.bg = bg # bas-gauche
        self.bd = bd # bas-droite
    
    def __str__(self, prefix=""):
        return "\n".join((f"{prefix}({self.x},{self.y},{self.l},{self.h}) couleur ({self.r},{self.v},{self.b}) enfants :",
            self.hg.__str__(prefix+"  ") if self.hg!=None else prefix+"  None",
            self.hd.__str__(prefix+"  ") if self.hd!=None else prefix+"  None",
            self.bg.__str__(prefix+"  ") if self.bg!=None else prefix+"  None",
            self.bd.__str__(prefix+"  ") if self.bd!=None else prefix+"  None"))

    # ------------------------------------------------------------------#
    #    fonction arbre et peindre_arbre initiales                      #
    #-------------------------------------------------------------------#
def arbre1(px, x, y, w, h, seuil):
    r, g, b = moyenne(px, x, y, w, h)
    if homogeneite(px, x, y, w, h, seuil):
        return Noeud1(x, y, w, h, r, g, b, None, None, None, None)
    else:
        hg, hd, bg, bd = partition(x, y, w, h)
        return Noeud1(x, y, w, h, r, g, b,
            arbre1(px, *hg, seuil) if hg!=None else None,
            arbre1(px, *hd, seuil) if hd!=None else None,
            arbre1(px, *bg, seuil) if bg!=None else None,
            arbre1(px, *bd, seuil) if bd!=None else None)
def peindre_arbre1(px, n):
    if n == None:
        return
    if n.hg==n.hd==n.bg==n.bd==None:
        peindre(px, n.x, n.y, n.l, n.h, (round(n.r), round(n.v), round(n.b)))
    else:
        peindre_arbre1(px, n.hg)
        peindre_arbre1(px, n.hd)
        peindre_arbre1(px, n.bg)
        peindre_arbre1(px, n.bd)
    # ------------------------------------------------------------------------------------------#
    #    fonction arbre et peindre_arbre de manière implicite                                   #
    # on applique le même principe que précedemmment :                                          #
    # - tant que la zone n'est pas homogène, on la découpe et on rapplique l'algo aux 4 parties #
    # - on peint directement les zones homogènes et on les ajoutes à la liste                   #
    # - arbre renvoie ainsi la liste de toutes les régions homogènes(plus de None)              #
    # définir une fonction dans la fonction permet d'ajouter les élements à la liste            #
    #-------------------------------------------------------------------------------------------#
    
def arbre(x,y,w,h,seuil,px):
    L=[] #initialisation de la liste 
    def peindre_arbre(x,y,w,h,seuil,px): # fonction générant les regions homogènes
        if homogeneite(px,x,y,w,h,seuil) :
            r,g,b=moyenne(px,x,y,w,h)
            peindre(px,x,y,w,h,(round(r),round(g),round(b)))
            L.append(Noeud(x,y,w,h,r,g,b))
        else:
            (a,b,c,d)=partition(x, y, w, h)
            if a!=None:
                peindre_arbre(*a,seuil,px)
            if b!=None:
                peindre_arbre(*b,seuil,px)
            if c!=None:
                peindre_arbre(*c,seuil,px)
            if d!=None:
                peindre_arbre(*d,seuil,px)
    peindre_arbre(x,y,w,h,seuil,px)
    return L

    # ----------------------------------------------------------------------------------#
    #    fonction arbre et peindre_arbre tenant compte de la fonction homogène modifié  #
    #-----------------------------------------------------------------------------------#
def arbre_modifié(x,y,w,h,seuil,px):
    L=[]
    x0,y0= floor(x//2),floor(y//2)
    def peindre_arbre(x,y,w,h,seuil,px):
        if homogeneite_modifie(px,x,y,w,h,x0,y0,seuil) :
            r,g,b=moyenne(px,x,y,w,h)
            peindre(px,x,y,w,h,(round(r),round(g),round(b)))
            L.append(Noeud(x,y,w,h,r,g,b))
        else:
            (a,b,c,d)=partition(x, y, w, h)
            if a!=None:
                peindre_arbre(*a,seuil,px)
            if b!=None:
                peindre_arbre(*b,seuil,px)
            if c!=None:
                peindre_arbre(*c,seuil,px)
            if d!=None:
                peindre_arbre(*d,seuil,px)
    peindre_arbre(x,y,w,h,seuil,px)
    return L

def peindre_profondeur(px, n, m, p=0):
    if n == None:
        return
    if n.hg==n.hd==n.bg==n.bd==None:
        peindre(px, n.x, n.y, n.l, n.h, (255*p//m, 255*p//m, 255*p//m))
    else:
        peindre_profondeur(px, n.hg, m, p+1)
        peindre_profondeur(px, n.hd, m, p+1)
        peindre_profondeur(px, n.bg, m, p+1)
        peindre_profondeur(px, n.bd, m, p+1)
        
    # ------------------------------------------------------------------#
    #    fonction Ecart quadratique non recursive                       #
    # elle prend tous pixels un par un et somme les ecarts quadratiques #
    #-------------------------------------------------------------------#

def EQ(px1,px,W,H):
        eq = 0   
        for i in range(W):
            for j in range(H):
                
                r, g, b = px[i, j][0:3]
                r1,g1,b1= px1[i, j][0:3]
                eq += (r-r1)**2 + (g-g1)**2 + (b-b1)**2
        return eq
    # ------------------------------------------------------------------#
    #    fonction PSNR non recursive                                    #
    # calcul le PSNR avec EQ définit ci-dessus                          #
    #-------------------------------------------------------------------#

def PSNR(px1,px,W,H):
    return 20 * log10(255) - 10 * log10(EQ(px1,px,W,H) / (3*W*H) )
    # ------------------------------------------------------------------#
    #    fonctions permettant de réaliser la fonction flou              #
    # voir rapport pour explication                                     #
    #-------------------------------------------------------------------#
   
def get_couleur(px,x,y):
    r,v,b = px[x,y][0:3]
    return (r,v,b)

def moyenne_autour(px,L):
    n = len(L)
    s = [0,0,0]
    for el in L:
        s[0]+=el[0]
        s[1]+=el[1]
        s[2]+=el[2]
    return(s[0]/n,s[1]/n,s[2]/n)
        
def flou(px,w,h):
    
    
    for i in range (w):
        for j in range (h):
            v = voisins(px, i, j)
            C = []
            for k in range (len(v)):
                C.append(get_couleur(px,v[k][0],v[k][1]))
            m =  moyenne_autour(px,C) 
            m_entier = (ceil(m[0]),ceil(m[1]),ceil(m[2]))
            px[i,j] = m_entier
            
    
def voisins(px, x, y):
    w,h = im.size
    L = []
        #for dx, dy in ((1,1), (1,0), (0,1), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1))
    for dx, dy in ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)):
        if 0 <= x+dx < w and 0 <= y+dy < h:
            L.append([x+dx,y+dy])
    return L
               
if __name__ == '__main__': 
    # ------------------------------------------------#
    #   pour le graphes  avec la methode des noeuds   #
    #-------------------------------------------------#
    """
    L=[]
    M=[]
    for i in range (51):
        im = Image.open("lyon.png")
        W, H = im.size
        px = im.load()
        s=20+i
        start=time.process_time()
        T=arbre1(px,0,0,W,H,s)
        peindre_arbre1(px, T)
        end=time.process_time()
        M+=[s]
        L+=[end-start]
    plt.plot(M,L)
    plt.xlabel("Seuil")
    plt.ylabel("Temps d'exécution")
    plt.title("Performance temporelle")
    """
    # ------------------------------------------------#
    #               pour les graphes                  #
    #-------------------------------------------------#
    """
    L=[]
    M=[]
    for i in range (51):
        im = Image.open("lyon.png")
        W, H = im.size
        px = im.load()
        s=20+i
        start=time.process_time()
        T=arbre(0,0,W,H,s,px)
        end=time.process_time()
        M+=[s]
        L+=[end-start]
    plt.plot(M,L)
    plt.xlabel("Seuil")
    plt.ylabel("Temps d'exécution")
    plt.title("Performance temporelle")
    """
    # --------------------------------------------------------------#
    #        test de PSNR avec la nouvelle fonction homogeneite     #                  
    #---------------------------------------------------------------#
    
    """
    im = Image.open("grenouille.png")
    px = im.load() # importation des pixels de l’image
    W, H = im.size
    s=10
    T=arbre_modifié(0,0,W,H,s,px)
    im.save("grenouille_modi1.png")
    im = Image.open("grenouille.png")
    px = im.load() # importation des pixels de l’image
    im1 = Image.open("grenouille_modi1.png")
    px1= im1.load()
    print(PSNR(px1, px, W, H))
    """
    
    # --------------------------------------------------------------#
    #        test de la fonction flou sur l'image Lyon              #                  
    #---------------------------------------------------------------#
    """
    im = Image.open("lyon.png")
    px = im.load() # importation des pixels de l’image
    W, H = im.size
    flou(px, W, H)
    im.save("lyon_flou.png")
    """
    
    # --------------------------------------------------------------------#
    # test de PSNR combinaison de homogeneite + flou sur la grenouille    #                  
    #---------------------------------------------------------------------#
    """
    im = Image.open("grenouille.png")
    px = im.load() # importation des pixels de l’image
    W, H = im.size
    s=10
    T=arbre(0,0,W,H,s,px)
    flou(px, W, H)
    im.save("grenouille_homogeneite_flou_flou.png")
    im = Image.open("grenouille.png")
    px = im.load() # importation des pixels de l’image
    im1 = Image.open("grenouille_modi_flou.png")
    px1= im1.load()
    print(PSNR(px1, px, W, H))
    """
    
    
     
    
    
   
              
              