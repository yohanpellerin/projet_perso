#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 16:19:17 2021

@author: yohanpellerin
"""


import http.server
import socketserver
import sqlite3
# définition du nouveau handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    
 # sous-répertoire racine des documents statiques
     static_dir = '/client'
 # on surcharge la méthode qui traite les requêtes GET
     def do_GET(self):
         
         if self.path=="/time":
             time = self.date_time_string()
             self.send(time)
         elif self.path=="/sites":
             self.__conn= sqlite3.connect("sites.db")
             curseur=self.__conn.cursor()
             curseur.execute("SELECT name FROM sites ")
             a=""
             for elt in curseur.fetchall():
                 a+=str(elt[0]) +"\n"
            self.send(a)
        
                 
         
 # on modifie le chemin d'accès en insérant un répertoire préfixe
         self.path = self.static_dir + self.path
 # on traite la requête via la classe parent
         http.server.SimpleHTTPRequestHandler.do_GET(self)
# instanciation et lancement du serveur
     def send(self,body,headers=[]):

    # on encode la chaine de caractères à envoyer
       encoded = bytes(body, 'UTF-8')
 
    # on envoie la ligne de statut
       self.send_response(200)

    # on envoie les lignes d'entête et la ligne vide
       [self.send_header(*t) for t in headers]
       self.send_header('Content-Length',int(len(encoded)))
       self.end_headers()

    # on envoie le corps de la réponse
       self.wfile.write(encoded)

httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()
