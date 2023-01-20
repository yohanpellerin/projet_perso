#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:47:38 2021

@author: yohanpellerin
"""

from tkinter import *
from random import randint
from forme import *
from tkinter.colorchooser import askcolor

class FenPrincipale(Tk):


    def __init__(self):
        Tk.__init__(self)
        self.__mot = ""
        self.__motaffiché=""
        self.__bouton=[]
        self.__nbmanqué=0
        self.__dernierbouton=[] #liste contenant les boutons utilisés 
        self.__fin=0 # entier permettant de déterminer si la partie est gagné (1), perdu (2) et pas terminé (0)
        
        
        # paramètres de la fenêtre
        self.title('jeu du pendu')
        self.geometry('1000x600+400+400')
        self.configure(bg="blue")

        # constitution de l'arbre de scène
        barreoutil= Frame(self)
        barreoutil.pack(side=TOP)
        self.__Zone_daffichage= ZoneAffichage(self, 800, 400)
        self.__Zone_daffichage.pack(side=TOP,padx=5, pady=5)
        self.__Zone_daffichage.configure(bg="white")
        self.__textmot=Label(self,text="")
        self.__textmot.pack(side=TOP)
        clavier= Frame(self)
        clavier.pack(side=BOTTOM)


        boutonLancer = Button(barreoutil, text='Nouvelle partie')
        boutonLancer.pack(side=LEFT, padx=5, pady=5)
        boutonLancer.config(command=self.nouvelle_partie)
        boutonquitter = Button(barreoutil, text='Quitter')
        boutonquitter.pack(side=LEFT, padx=5, pady=5)
        boutonquitter.config(command=self.destroy)
        
        
#-----------------------------------------------------------------------------------------------------#       
#                                Définition du bouton pour la fonction Undo                           #                                          #
#-----------------------------------------------------------------------------------------------------#                                                                                                    #


        boutonUndo=Button(barreoutil, text='Undo')
        boutonUndo.pack(side=LEFT, padx=5, pady=5)
        boutonUndo.config(command=self.Undo)
        
#-----------------------------------------------------------------------------------------------------#       
#                                Définition du bouton pour la fonction Couleur Background             #                                          #
#-----------------------------------------------------------------------------------------------------#                                                                                                    #
       
        
        bouton_Couleur_bg=Button(barreoutil, text='Couleur background')
        bouton_Couleur_bg.pack(side=LEFT, padx=5, pady=5)
        bouton_Couleur_bg.config(command=self.changer_couleur_bg)#la commande agit dans la fenêtre
        
#-----------------------------------------------------------------------------------------------------#       
#                                Définition du bouton pour la fonction Couleur zone de jeu            #                                          #
#-----------------------------------------------------------------------------------------------------#                                                                                                    #
        
        
        bouton_Couleur_jeu=Button(barreoutil, text='Couleur zone de jeu')
        bouton_Couleur_jeu.pack(side=LEFT, padx=5, pady=5)
        bouton_Couleur_jeu.config(command=self.__Zone_daffichage.changer_couleur_jeu) #la commande agit dans le Canvas
#-----------------------------------------------------------------------------------------------------#       
#                                Définition du bouton pour la fonction change couleur potence            #                                          #
#-----------------------------------------------------------------------------------------------------#   

        bouton_Couleur_potence=Button(barreoutil, text='Couleur potence')
        bouton_Couleur_potence.pack(side=LEFT, padx=5, pady=5)
        bouton_Couleur_potence.config(command=self.__Zone_daffichage.changer_couleur_potence) #la commande agit dans le Canvas
#-----------------------------------------------------------------------------------------------------#       
#                                Définition du bouton pour la fonction change couleur pendu            #                                          #
#-----------------------------------------------------------------------------------------------------#   
        bouton_Couleur_pendu=Button(barreoutil, text='Couleur pendu')
        bouton_Couleur_pendu.pack(side=LEFT, padx=5, pady=5)
        bouton_Couleur_pendu.config(command=self.__Zone_daffichage.changer_couleur_pendu) #la commande agit dans le Canvas

#-----------------------------------------------------------------------------------------------------#       
#                               Mise en place du clavier                                              #
#-----------------------------------------------------------------------------------------------------#

        for i in range (0,26):
             t = chr(ord('A')+i)
             self.__bouton.append(MonBoutonLettre(clavier,self,t,2))
             if i<=20:
                 a=i//7
                 b=i%7
                 self.__bouton[i].grid(row=a, column=b) 
                 self.__bouton[i].config(state=DISABLED)
             else:
                b=i-20
                self.__bouton[i].grid(row=4, column=b)
                self.__bouton[i].config(state=DISABLED)

        self.chargeMots()
        
#-----------------------------------------------------------------------------------------------------#       
#                       Modification de la fonction nouvelle partie pour implémenter Undo                                         #                                          #
#-----------------------------------------------------------------------------------------------------#                                                                                                    #
        
    def nouvelle_partie(self):
        for i in range (0,26):
             self.__bouton[i].config(state=NORMAL)
        self.__mot=self.__mots[randint(0,len(self.__mots)-1)]
        self.__motaffiché=len(self.__mot)*'*'
        self.__textmot["text"]='Mot : ' + self.__motaffiché
        self.__nbmanqué=0
        for i in range(26):
             self.__bouton[i].config(command=self.__bouton[i].cliquer)
        self.__Zone_daffichage.cachePendu()
        self.__dernierbouton=[] # remise à zéro de l'historique 

#-----------------------------------------------------------------------------------------------------#       
#                                Bloc de la fonction Undo                                             #                                          
#-----------------------------------------------------------------------------------------------------#                                                                                                    #

    def Undo(self):
        if self.__dernierbouton != []: # on verifie qu'un bouton a été joué
            if self.__fin==0: # on se place dans le cas où la partie n'est pas terminée
                
                if self.__dernierbouton[len(self.__dernierbouton)-1][1]==0: #teste si le bouton correspond à une lettre absente

                    self.__Zone_daffichage.cachepiece(self.__nbmanqué)#cache la dernière pièce
                    self.__nbmanqué += -1#décrémente nbManqué
                    self.__bouton[ord(self.__dernierbouton[len(self.__dernierbouton)-1][0])-ord('A')].config(state=NORMAL)#remet l'état du bouton sur normal
                    self.__dernierbouton.remove(self.__dernierbouton[len(self.__dernierbouton)-1])#supprime le dernier bouton utilisé

                else : # le bouton correspond à une lettre présente dans le mot 

                    self.__bouton[ord(self.__dernierbouton[len(self.__dernierbouton)-1][0])-ord('A')].config(state=NORMAL)#dégrise le bouton
                    
                    self.__dernierbouton.remove(self.__dernierbouton[len(self.__dernierbouton)-1])#supprime le dernier bouton utilisé
                
                    #------------------------------------------------------------------------------#       
                    #                                Re-création du mot affiché                    #                                          
                    #------------------------------------------------------------------------------#
                
      
                    self.__motaffiché=len(self.__mot)*'*' #on inialise mot affiché avec seulement des *
                
                    for i in range (len(self.__dernierbouton)): # pour chaque lettre selectionnée avant 
                        if self.__dernierbouton[i][1]==1: # on regarde si la lettre est dans le mot                                     
                        
                            lettres=list(self.__motaffiché)  #de la même manière que dans la fonction traitement, on modifie self.__motaffiché                                                                    
                            A=self.__dernierbouton[i][0]                        
                            for i in range(len(self.__mot)):                           
                                if self.__mot[i]==A:
                                    lettres[i]=A
                            self.__motaffiché=''.join(lettres)
                    self.__textmot["text"]='Mot : ' + self.__motaffiché #on modifie le label pour faire correspondre le mot
            else:  # si la partie est finie
            
                    #------------------------------------------------------------------------------#       
                    #                               On réactive tous les boutons                   #                                          
                    #------------------------------------------------------------------------------#
                for i in range(26):
                    self.__bouton[i].config(state=NORMAL)
                    
                if self.__fin==2: # si on avait perdu
                   
                    self.__Zone_daffichage.cachepiece(self.__nbmanqué)#cache la dernière pièce
                    self.__nbmanqué += -1#décrémente nbManqué
                    self.__dernierbouton.remove(self.__dernierbouton[len(self.__dernierbouton)-1])#supprime le dernier bouton utilisé
                    
                   
                else: # si on avait gagné
                    
                    self.__dernierbouton.remove(self.__dernierbouton[len(self.__dernierbouton)-1])#supprime le dernier bouton utilisé
                    #------------------------------------------------------------------------------#       
                    #                On affiche le mot sans la dernière lettre trouvée             #                                          
                    #------------------------------------------------------------------------------#
                    
                    self.__motaffiché=len(self.__mot)*'*' #on inialise mot affiché avec seulement des *
                
                    for i in range (len(self.__dernierbouton)): # pour chaque lettre selectionnée avant 
                        if self.__dernierbouton[i][1]==1: # on regarde si la lettre est dans le mot                                     
                        
                            lettres=list(self.__motaffiché)  #de la même manière que dans la fonction traitement, on modifie self.__motaffiché                                                                    
                            A=self.__dernierbouton[i][0]                        
                            for i in range(len(self.__mot)):                           
                                if self.__mot[i]==A:
                                    lettres[i]=A
                            self.__motaffiché=''.join(lettres)
                 #------------------------------------------------------------------------------#       
                 #                               On grise tous les boutons déjà tombés          #                                          
                 #------------------------------------------------------------------------------#
                for i in range (len(self.__dernierbouton)):
                        self.__bouton[ord(self.__dernierbouton[i][0])-ord('A')].config(state=DISABLED)
                        
                        
                self.__fin=0 # la partie n'est plus fini                
                self.__textmot["text"]='Mot : ' + self.__motaffiché #on modifie le label pour faire correspondre le mot




    def chargeMots(self):
             f = open('mots.txt', 'r')
             s = f.read()
             self.__mots = s.split('\n')
             f.close()
             
#-----------------------------------------------------------------------------------------------------#       
#               Modification de la fonction traitement et finPartie pour implémenter Undo             #                                          
#-----------------------------------------------------------------------------------------------------#                                                                                                    
             
    def traitement(self,A):
        cpt=0
        lettres=list(self.__motaffiché)
        for i in range(len(self.__mot)):
            if self.__mot[i]==A:
                cpt=1
                lettres[i]=A
        self.__motaffiché=''.join(lettres)
        if cpt==0:
            self.__nbmanqué+=1
            self.__Zone_daffichage.ajoutpiece(self.__nbmanqué)
            if self.__nbmanqué>=10:
                self.finPartie(False)
                
                
            self.__dernierbouton+=[[A,0]]  #on ajoute à la liste le bouton et l'état 0 qui correspond à une lettre manquée
            
            
        else :
            self.__textmot["text"]='Mot : ' + self.__motaffiché
            if self.__motaffiché==self.__mot:
                self.finPartie(True)
                
                
            self.__dernierbouton+=[[A,1]] #on ajoute à la liste le bouton et l'état 1 qui correspond à une lettre présente
            

    def finPartie(self,A):
        for i in range(26):
            self.__bouton[i].config(state=DISABLED)
        if A==True :
            self.__textmot["text"]='Bravo vous avez gagné, le mot est :' + self.__motaffiché
            self.__fin=1 # permet de savoir la partie est finie est gagné
        else :
            self.__textmot["text"]='Vous avez perdu, le mot était :' + self.__mot
            self.__fin=2 # permet de savoir la partie est finie est perdu
            
            
#-----------------------------------------------------------------------------------------------------#       
#                           Bloc de la fonction de changement de couleur du Background                #                                          #
#-----------------------------------------------------------------------------------------------------# 
    def changer_couleur_bg(self):
        colors = askcolor(title="Choix de la couleur du background") # on ouvre le panneau de choix des couleurs grâce à askcolor de TKinter
        self.configure(bg=colors[1]) #on modifie la couleur en utilisant le choix de l'utilisateur



class MonBoutonLettre(Button):
    def __init__(self,parent,grandparent,A,b):
        Button.__init__(self,master=parent,text=A, width=b)
        self.__lettre=A
        self.__gp=grandparent
    def cliquer(self):
        self.config(state=DISABLED)
        self.__gp.traitement(self.__lettre)



class ZoneAffichage(Canvas):
    
    
    def __init__(self, parent, largeur, hauteur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur)
        self.__listeShape=[]
        # Base, Poteau, Traverse, Corde
        self.__listeShape.append(Rectangle(self, 50,  270, 200,  26, "brown"))
        self.__listeShape.append(Rectangle(self, 87,   83,  26, 200, "brown"))
        self.__listeShape.append(Rectangle(self, 87,   70, 150,  26, "brown"))
        self.__listeShape.append(Rectangle(self, 183,  67,  10,  40, "brown"))
        # Tete, Tronc
        self.__listeShape.append(Rectangle(self, 188, 120,  20,  20, "black"))
        self.__listeShape.append(Rectangle(self, 175, 143,  26,  60, "black"))
        # Bras gauche et droit
        self.__listeShape.append(Rectangle(self, 133, 150,  40,  10, "black"))
        self.__listeShape.append(Rectangle(self, 203, 150,  40,  10, "black"))
        # Jambes gauche et droite
        self.__listeShape.append(Rectangle(self, 175, 205,  10,  40, "black"))
        self.__listeShape.append(Rectangle(self, 191, 205,  10,  40, "black"))

    def cachePendu(self):
        for i in range (len(self.__listeShape)):
            self.__listeShape[i].setState("hidden")

    def ajoutpiece(self,i):
        if i<=len(self.__listeShape):
            self.__listeShape[i-1].setState("normal")
    
#-----------------------------------------------------------------------------------------------------#       
#                           Bloc de la fonction cachepièce (utilisé dans Undo                         #          
#-----------------------------------------------------------------------------------------------------# 
    def cachepiece(self,i):
        if i<=len(self.__listeShape): # verifie que la pièce a cacher est dans la liste 
            self.__listeShape[i-1].setState("hidden") #on la cache 
            
            
#-----------------------------------------------------------------------------------------------------#       
#                           Bloc de la fonction de changement de couleur de la zone de jeu            #                                          
#-----------------------------------------------------------------------------------------------------#            

    def changer_couleur_jeu(self):
        colors = askcolor(title="Choix de la couleur de la zone de jeu")# on ouvre le panneau de choix des couleurs grâce à askcolor de TKinter
        self.configure(bg=colors[1]) #on modifie la couleur en utilisant le choix de l'utilisateur
        
#-----------------------------------------------------------------------------------------------------#       
#                           Bloc de la fonction de changement de couleur de la zone de jeu            #                                          
#-----------------------------------------------------------------------------------------------------#     
    def changer_couleur_potence(self):
        colors = askcolor(title="Choix de la couleur de la potence") # on ouvre le panneau de choix des couleurs grâce à askcolor de TKinter
        
        #-----------------------------------------------------------------------------------------------------#       
        # Pour chaque piece de listeShape on regarde si elle etait cachée ou non pour cela on a rajouté       #
        #        un attribut(public) aux formes : state permettant de savoir si ils sont cachée ou non        #                                          
        #-----------------------------------------------------------------------------------------------------#   
        if self.__listeShape[0].state=="hidden": # la pièce est cachée
                self.__listeShape[0]=Rectangle(self, 50,  270, 200,  26, colors[1]) #on change la couleur de la pièce
                self.__listeShape[0].setState("hidden") # on la cache 
        else: # la pièce n'est pas caché initialement 
                self.__listeShape[0].setState("hidden") # on la cache 
                self.__listeShape[0]=Rectangle(self, 50,  270, 200,  26, colors[1])  #on change la couleur de la pièce
        # on applique le même principe pour les autres pièces       
        if self.__listeShape[1].state=="hidden":
                self.__listeShape[1]=Rectangle(self, 87,   83,  26, 200, colors[1])
                self.__listeShape[1].setState("hidden")
        else:
                self.__listeShape[1].setState("hidden")
                self.__listeShape[1]=Rectangle(self, 87,   83,  26, 200, colors[1])
                
        if self.__listeShape[2].state=="hidden":
                
                self.__listeShape[2]=Rectangle(self, 87,   70, 150,  26, colors[1])
                self.__listeShape[2].setState("hidden")
        else:
                self.__listeShape[2].setState("hidden")
                self.__listeShape[2]=Rectangle(self, 87,   70, 150,  26, colors[1])
                
        if self.__listeShape[3].state=="hidden":
                self.__listeShape[3]=Rectangle(self, 183,  67,  10,  40, colors[1])
                self.__listeShape[3].setState("hidden")
        else:
                self.__listeShape[3].setState("hidden")
                self.__listeShape[3]=Rectangle(self, 183,  67,  10,  40, colors[1])
               
#-----------------------------------------------------------------------------------------------------#       
#                           Bloc de la fonction de changement de couleur de la zone de jeu            #        
#                                (même principe que precedemment)                                      #
#-----------------------------------------------------------------------------------------------------#     
    def changer_couleur_pendu(self):
        colors = askcolor(title="Choix de la couleur de la pendu")
        
        if self.__listeShape[4].state=="hidden":
                self.__listeShape[4]=Rectangle(self, 188, 120,  20,  20, colors[1])
                self.__listeShape[4].setState("hidden")
        else:
                self.__listeShape[4].setState("hidden")
                self.__listeShape[4]=Rectangle(self, 188, 120,  20,  20, colors[1])
                
        if self.__listeShape[5].state=="hidden":
                self.__listeShape[5]=Rectangle(self, 175, 143,  26,  60, colors[1])
                self.__listeShape[5].setState("hidden")
        else:
                self.__listeShape[5].setState("hidden")
                self.__listeShape[5]=Rectangle(self, 175, 143,  26,  60, colors[1])
                
        if self.__listeShape[6].state=="hidden":
                
                self.__listeShape[6]=Rectangle(self, 133, 150,  40,  10, colors[1])
                self.__listeShape[6].setState("hidden")
        else:
                self.__listeShape[6].setState("hidden")
                self.__listeShape[6]=Rectangle(self, 133, 150,  40,  10, colors[1])
                
        if self.__listeShape[7].state=="hidden":
                self.__listeShape[7]=Rectangle(self, 203, 150,  40,  10, colors[1])
                self.__listeShape[7].setState("hidden")
        else:
                self.__listeShape[7].setState("hidden")
                self.__listeShape[7]=Rectangle(self, 203, 150,  40,  10, colors[1])
                
        if self.__listeShape[8].state=="hidden":
                
                self.__listeShape[8]=Rectangle(self, 175, 205,  10,  40, colors[1])
                self.__listeShape[8].setState("hidden")
        else:
                self.__listeShape[8].setState("hidden")
                self.__listeShape[8]=Rectangle(self, 175, 205,  10,  40, colors[1])
                
        if self.__listeShape[9].state=="hidden":
                self.__listeShape[9]=Rectangle(self, 191, 205,  10,  40, colors[1])
                self.__listeShape[9].setState("hidden")
        else:
                self.__listeShape[9].setState("hidden")
                self.__listeShape[9]=Rectangle(self, 191, 205,  10,  40, colors[1])
        
if __name__ == '__main__':

    app = FenPrincipale()
    app.mainloop()
