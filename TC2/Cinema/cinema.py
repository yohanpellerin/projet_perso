#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 15:51:49 2021

@author: yohanpellerin
"""
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
class Film:
    
    def __init__(self,bdd):
        try:
            self.__conn = sqlite3.connect(bdd)  
            self.__curseur=self.__conn.cursor()
        except Exception as err:                                
            print('err:', str(err))
            print('type exception:', type(err).__name__)

        
        
    def __del__ (self):
        self.__conn.close()
        
    def get_score_moy_par_annee (self,acteur):
        
            L=[]
            for i in range(0,10):  #Pour chaque trache de 5 années
                a1= 1951+ 5*i      #on cherche la moyenne des films d'un acteur
                a2=a1+4           
                arg="SELECT avg(score)  FROM films JOIN distributions JOIN acteurs ON idfilm=films.id and idacteur=acteurs.id where nom == '{}' and annee<= {} and annee>= {}".format(acteur,a2,a1)
                self.__curseur.execute(arg)
                if self.__curseur.fetchall()==[(None,)]:  # si il n'a pas fait de film
                    L=L+[0] #on remplace par 0 le None
                else:
                    self.__curseur.execute(arg)
                    a=self.__curseur.fetchall()
                    L=L+[a[0][0]]    #sinon on modifie le résultat pour l'avoir sous forme de liste 
            return (L) 
    def get_top_3_decennie(self,a1):
        
            arg="SELECT titre, nom, score FROM films JOIN realisateurs ON idrealisateur=realisateurs.id WHERE annee>={} AND annee<={} ORDER BY score DESC LIMIT 3".format(a1,a1+10)
            self.__curseur.execute(arg)  # on recupère les 3 meilleurs réalisateurs de la décennies, le film et le score
            L=self.__curseur.fetchall()
            reali_film=[]
        
            score=[]
            for i in range (0,3):
                reali_film= reali_film+ [L[i][1]+'\n' + L[i][0]] #on crée une liste avec le realisateur et le film
                score= score + [L[i][2]] # et une avec simplement le score
            return(score,reali_film)
      

if __name__ == '__main__':
    afilm=Film('films.sqlite3') # on initialise 
    barWidth = 0.3
    acteur1='Harrison Ford' # les acteurs à comparer
    acteur2='Morgan Freeman'
    acteurs=(acteur1,acteur2)
    y1 = afilm.get_score_moy_par_annee(acteur1) #ordonnés pour l'acteur 1
    y2 = afilm.get_score_moy_par_annee(acteur2) #ordonnés pour l'acteur 2
    r1 = range(len(y1))
    r2 = [x + barWidth for x in r1]
    if y1 != [0]*10 and y2 != [0]*10: # si il n'y a que des 0 c'est que l'acteur n'esty pas dans la table
        plt.bar(r1, y1, width = barWidth, color = ['blue' for i in y1], linewidth = 10)
        plt.bar(r2, y2, width = barWidth, color = ['green' for i in y1], linewidth = 10)
        M=[]
        for i in range (0,10):
            a=1951+5*i
            b=a+4           # on crée les abscisses
           
            M=M+[ "{} \n {} ".format(a,b)]
        plt.xticks([r + barWidth / 2 for r in range(len(y1))],M)
        plt.ylabel('Score moyen')
        plt.xlabel('Années')
        plt.title('Comparaison') #titre
        plt.legend(acteurs,loc=(0.70,1))  #positionnement de la légende
        plt.show()
      
    else:
        print("un des deux noms n'est pas dans la liste") 

    plt.close("all")
    a1="l" # choix de l'année qui va déterminer la décennie 
    try:
        
        assert a1 >= 1951 , "l'année doit être compriseentre 1951 et 2000" #on verfie qu'il s'agisse d'une decennie dans la table
        assert a1 <= 2000 , "l'année doit être compriseentre 1951 et 2000"
        x = afilm.get_top_3_decennie(a1)[0] # la liste des noms et films

        rank =afilm.get_top_3_decennie(a1)[1]

        plt.bar(rank, x)
        arg="Score des 3 meilleurs films entre {} et {}".format(a1,a1+10) #titre
        plt.title(arg)
        plt.ylabel('Score')
        plt.show()
        
    except AssertionError as msg: print(msg)
    except TypeError as e:
            print("il doit s'agir d'un entier") # si on ne met pas un entier dans a1


    




    