#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 14:05:09 2021

@author: yohanpellerin
"""
import time
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from math import *
from copy import*

    #---------------------------------------------------------#
    #            fonction créer pendant le TD                 #
    #---------------------------------------------------------#  
def glouton(S, M, D):
    if M<S[0]: return None

    T = [0]*len(S)

    for i in range(len(S)-1, -1, -1):
        # if M-S[i]>=0:
        d,r = divmod(M, S[i])
        d = min(d, D[i])
        D[i] -= d
        M -= d*S[i]
        T[i] = d

    if M>0: return None

    return T

def Monnaie_graphe(M,S):
    Arbre={}
    Arbre[M]={}
    File=[M]
    
    M_restant=M
    while M_restant>0 and len(File)>0 :
        M_restant= File.pop(0)
        for s in S:
            M_fils=M_restant-s
            if M_fils>=0:
                Arbre[M_restant][M_fils]=s
               
                if M_fils not in Arbre:
                    Arbre[M_fils]={}
                    File.append(M_fils)
    return Arbre
def Plus_court_chemin(Arbre, M):

    chemin = []

    cible = 0
    while sum(chemin) != M: 
        for branche in Arbre:
            if cible in Arbre[branche]:
                chemin.append(Arbre[branche][cible])
                cible = branche
                break
        print("  branche = ", branche)
        print("  chemin = ", chemin)
        input('attente')

    return chemin

def Monnaie_graphe(S, M):
    Arbre = {}
    Arbre[M] = {}
    File = [M]

    M_restant = M
    while M_restant>0 and len(File)>0:
        
        M_restant = File.pop(0)
        for s in S:

            M_fils = M_restant-s

            if M_fils >= 0:

                if M_fils not in Arbre:
                    Arbre[M_fils] = {}
                    File.append(M_fils)

                Arbre[M_restant][M_fils] = s

    if len(File)==0: return None

    return Arbre

    #---------------------------------------------------------#
    #            fonction donnant la solution                 #
    #      du problème de minimisation du nombre de pièce     #
    #  dans le cas d'un nombre illimité de pieces disponible  #
    # elle renvoit le tableau et une liste contenant:         #
    #   le nombre de piece utilisée et les pièces utilisé     #
    #---------------------------------------------------------#  
    
def monnaie_bottom_up(S, M):
    # conditions aux bornes
    mat = [[[0,[0 for i in range (len(S))]] for i in range (M+1)] for i in range(len(S)+1)] 
    for m in range(M):
        mat[0][1+m][0] = M+1 # M+1=infini, car aucun rÃ©sultat valide ne dÃ©passe M
        
    # remplissage de la matrice par ordre topologique
    for i, v in enumerate(S):
        for m in range(1, M+1):
            if mat[i][m][0]<= 1+mat[i+1][m-v][0] if m-v>=0 else M+1:                
                mat[i+1][m] = deepcopy(mat[i][m])
            else:
                h=deepcopy(mat[i+1][m-v][1])
                h[i]= h[i]+1
                mat[i+1][m]=[1+mat[i+1][m-v][0],h]
    return mat, mat[len(S)][M]

    #---------------------------------------------------------#
    #            fonction donnant la solution                 #
    #      du problème de minimisation du nombre de pièce     #
    #    dans le cas d'un nombre limité de pieces disponible  #
    # elle renvoit le tableau et une liste contenant:         #
    #   le nombre de piece utilisée et les pièces utilisé     #
    #         ainsi que les pièces encore disponible          #
    #---------------------------------------------------------#  


def monnaie_bottom_up_limité(S,M,D):
    # conditions aux bornes
    mat = [[[0,[0 for i in range (len(S))],D] for i in range (M+1)] for i in range(len(S)+1)] 
    for m in range(M):
        mat[0][1+m][0] = M+1 # M+1=infini, car aucun rÃ©sultat valide ne dÃ©passe M
    # remplissage de la matrice par ordre topologique
    for i, v in enumerate(S):
        for m in range(1, M+1):
            a=0
            k=0
            while mat[i][m-k*v][2][i]>=k and m-k*v>=0:   
                if a+mat[i][m-a*v][0]>= k+mat[i][m-k*v][0]:
                    a=k
                k=k+1
                
            mat[i+1][m][0]=a+mat[i][m-a*v][0]
            h=deepcopy(mat[i][m-a*v][1])
            h[i]= h[i]+a
            mat[i+1][m][1]=deepcopy(h)
            q=deepcopy(mat[i][m-a*v][2])
            q[i]= q[i]-a
            mat[i+1][m][2]=deepcopy(q)
    return mat, mat[len(S)][M]

    #---------------------------------------------------------#
    #          fonction donnant la solution                   #
    #      du problème de minimisation du poids               #
    #  elle renvoit le tableau et une liste contenant :       #
    #         le piods et les pièces utilisé                  #
    #---------------------------------------------------------#  
                    
def monnaie_poids(P,S,M):
    # conditions aux bornes
    mat = [[[0,[0 for i in range (len(P))]] for i in range (M+1)] for i in range(len(S)+1)] 
    for m in range(M):
        mat[0][1+m][0] = 1000000 # =infini, car aucun rÃ©sultat valide ne dÃ©passe M
        
    # remplissage de la matrice par ordre topologique
    for i, v in enumerate(S):
        for m in range(1, M+1):
            if mat[i][m][0]<= P[i]+mat[i+1][m-v][0] if m-v>=0 else M+1:                
                mat[i+1][m] = deepcopy(mat[i][m])
            else:
                h=deepcopy(mat[i+1][m-v][1])
                h[i]= h[i]+1
                mat[i+1][m]=[P[i]+mat[i+1][m-v][0],h]
    return mat, mat[len(S)][M]

    #---------------------------------------------------------#
    #      fonction permettant d'affiche la solution          #
    #    du problème de minimisation du nombre de pièce       #
    #---------------------------------------------------------#  
                    
def affichage_nb_de_piece(L,S):
    M=[]
    for i in range (len(L[1])):
        if L[1][i]!=0:
            M=M+[[S[i],L[1][i]]]
    if len(M)==0:
        return "aucune solution n'est possible"
    S="nb_pieces_min : " + str(L[0]) + '\n' 'Une combinaison est:'+ '\n'
    for i in range (len(M)):
        S+= str(M[i][1]) + ' pièce(s) ou billet(s) de ' + str(M[i][0])+ '€ \n'
    return S
    #---------------------------------------------------------#
    #      fonction permettant d'affiche la solution          #
    #         du problème de minimisation du poids            #
    #---------------------------------------------------------#   

def affichage_poids(L,S):
    M=[]
    for i in range (len(L[1])):
        if L[1][i]!=0:
            M=M+[[S[i],L[1][i]]]
    if len(M)==0:
        return "aucune solution n'est possible"
    S="poids_min : " + str(L[0]) + ' g' + '\n' 'Une combinaison est:'+ '\n'
    for i in range (len(M)):
        S+= str(M[i][1]) + ' pièce(s) ou billet(s) de ' + str(M[i][0])+ '€ \n'
    return S
            
    #---------------------------------------------------------#
    #      fonction résolvant le problème de minimisation     #
    #           du poids de manière gloutonne                 #   
    #       elle renvoit uniquement le poids minimal          #  
    #---------------------------------------------------------#   
    
def poids_Gloutonne(P,S,M):
    L=[]
    for i in range (len(S)):
        j=i
        x=[P[i]/S[i],S[i],P[i]]
        L=L+[x]
        while j>0 and L[j-1][0]>x[0]:
            #Inv: Pour tout k vérifiant j<k<=i, L[k]>x
            L[j]=deepcopy(L[j-1])
            j-=1
            #Inv: Pour tout k vérifiant j<k<=i, L[k]>x
            L[j]=deepcopy(x)
            #Inv(i+1): L[0:i+1] est trié
    M2=M
    res=0
    for i in range (len(L)):
        if L[i][1]<=M2:
            res= res+ L[i][2]*(M2//L[i][1])
            M2=M2%L[i][1]
    return res


if __name__ == '__main__':
    
    #---------------------------------------------------------#
    #           test1: fonction monnaie_bottom_up             #
    #---------------------------------------------------------#

    
    S, M = [1, 7, 23], 28
    Mat, L = monnaie_bottom_up(S,M)
    print(affichage_nb_de_piece(L,S))

    
    #--------------------------------------------------------#
    #       test2 : fonction monnaie_bottom_up_limité        #
    #--------------------------------------------------------#
    

    S, M,D = [1, 7, 23], 28,[5,3,3]
    Mat, L = monnaie_bottom_up_limité(S,M,D)
    print(affichage_nb_de_piece(L,S))

    
    #--------------------------------------------------------#
    #       test3 : fonction monnaie_poids                   #
    #--------------------------------------------------------#
    

    P,S,M=[2.30,3.06,3.92,4.10,5.74,7.80,7.50,8.50,0.6,0.7,0.8,0.9,1],[1,2,5,10,20,50,100,200,500,1000,2000,5000,10000],7
    #P,S,M=[10,27,32,55],[1,3,4,7],6
    Mat, L =monnaie_poids(P,S,M)
    print(affichage_poids(L, S))   

    #-----------------------------------------------------------------#
    #  comparaison fonction monnaie_poids et poids_Gloutonne          #
    #-----------------------------------------------------------------#
   
    P,S=[10,27,32,55],[1,3,4,7]
    L='Les M tels que les algorithmes soient différents sont : \n'
    for i in range (21):
        Mat, poids_min1=monnaie_poids(P,S,i)
        poids_min2=poids_Gloutonne(P,S,i)
        if poids_min2!=poids_min1[0]:
            L=L+str(i)+' la fonction monnaie_poids donne '+ str(poids_min1[0]) + " g et l'autre " + str(poids_min2) + ' g \n'
    print(L)
    
    
     
           
                