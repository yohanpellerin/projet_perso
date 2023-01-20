#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 14:34:55 2021

@author: yohanpellerin
"""

class automate:
    def __init__(self,siema):
        self.__etat=[]
        self.__etat_initiale=""
        self.__etat_final=[]
        self.transition={}
        self.__motif=[]
        for s in siema:
            if s not in self.__motif:
                self.__motif.append(s)
                
        
    def ajout_etat(self,a,Z=False):
        if a not in self.__etat:
            self.__etat.append(a)
            self.transition[a]={}
        if self.__etat_initiale=="":
            self.__etat_initiale=a
        if Z==True:
            self.__etat_final.append(a)
        print(self.transition,)    
        
    def ajout_transition(self,etat1,motif,etat2):
        if motif in self.__motif and etat2 not in self.transition[etat1]:
            self.transition[etat1]={self.transition[etat1],etat2:motif}
        print(self.transition)  
    
    def recherche_etat(self,etat,symbol):
        if symbol not in self.__motif:
            return(False)
        
        
if __name__ == '__main__':  
    a = automate("abc")
    a.ajout_etat("0") 
    a.ajout_etat("1", True)
    
    a.ajout_transition("0", "b", "0")
    a.ajout_transition("0", "a", "1")
    a.ajout_transition("1", "a", "1") 
    a.ajout_transition("1", "b", "1")
    """
    assert a.run("abaaaaa") == True 
    assert a.run("bbb") == False"""