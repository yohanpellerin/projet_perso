#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 16:12:50 2021

@author: yohanpellerin
"""

from tkinter import *
from random import randint
from forme import *



        
class FenPrincipale(Tk):
    
    
        
    def __init__(self):
        Tk.__init__(self)
        self.forme=1
        
        # paramètres de la fenêtre
        self.title('tk')
        self.geometry('700x17000+400+400')
        self.configure(bg="grey")
        
        # constitution de l'arbre de scène
        barreoutil= Frame(self)
        barreoutil.pack(side=TOP)
        
        boutonLancer = Button(barreoutil, text='Rectangle')
        boutonLancer.pack(side=LEFT, padx=5, pady=5)
        boutonLancer1 = Button(barreoutil, text='Ellipse')
        boutonLancer1.pack(side=LEFT, padx=5, pady=5)
        boutonLancer2 = Button(barreoutil, text='Couleur')
        boutonLancer2.pack(side=LEFT, padx=5, pady=5)
        boutonLancer3 = Button(barreoutil, text='Quitter')
        boutonLancer3.pack(side=LEFT, padx=5, pady=5)
        fenetre= ZoneAffichage(self, 800, 1000)
        fenetre.pack(side=TOP,padx=5, pady=5)
        
        fenetre.bind("<ButtonRelease-1>", fenetre.ajout_forme)
        boutonLancer.config(command=fenetre.rect)
        boutonLancer1.config(command=fenetre.ellip)
        
    def clic(event):
        x=event.x
        y=event.y
        print(x,y)
    

class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur):
        Canvas.__init__(self, parent, width=largeur, height=hauteur)
        
    def ajout_forme(self,event):
        x=event.x
        y=event.y
        forme=self.forme
        if forme == 1:
       
            Rectangle(self,x,y,30,40,'black')
        else :
            
            Ellipse(self,x,y,30,40,'black')
    def rect(self):
        self.forme=1
    def ellip(self):
        self.forme=0
         
        
   
        
      

if __name__ == '__main__':
    
    app = FenPrincipale()
    app.mainloop()
