        # -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:50:54 2022

@author: pcau2
"""
import http.server
import socketserver
import sqlite3
import json
import datetime
import time
import math
from urllib.parse import unquote_plus

#
# Définition du nouveau handler
#
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    # sous-répertoire racine des documents statiques
    static_dir = '/client'
    #
    # On surcharge la méthode qui traite les requêtes GET
    #
    def do_GET(self):
        self.init_params()
        # le chemin d'accès commence par /time
        if self.path.startswith('/time'):
            self.send_time()
   


        # On se débarasse une bonne fois pour toutes du cas favicon.ico
        elif len(self.path_info) > 0 and self.path_info[0] == 'favicon.ico':
            self.send_error(204)

        # le chemin d'accès commence par le nom du projet au singulier, suivi par un nom de lieu
        elif len(self.path_info) > 1 and self.path_info[0] == entity_name:
            self.send_data(self.path_info[1])

        # le chemin d'accès commence par commentaires, suivi du point d'interêt
        elif len(self.path_info) > 1 and self.path_info[0] == "commentaires":
            self.send_commentaires_json()
            
        # le chemin d'accès commence par le nom de projet au pluriel
        elif len(self.path_info) > 0 and self.path_info[0] == entity_list_name:
            self.send_list()
            
        
      


        # ou pas...
        else:
            self.send_static()

    #
    # On surcharge la méthode qui traite les requêtes HEAD
    #
    def do_HEAD(self):
        self.send_static()




    # On surchage la méthode qui traite les requêtes POST
    def do_POST(self):
        self.init_params()
        
        # le chemin d'accès commence par commentaires, suivi du point d'interêt
        if len(self.path_info) > 0 and self.path_info[0] == "commentaire":
            self.post_comment()
        elif len(self.path_info) > 0 and self.path_info[0] == "register":
            self.post_register()
     
        # Method not supported
        else:
            self.send_error(405)
            
    
    def do_DELETE(self):
        self.init_params()
        
        if len(self.path_info)>1 and self.path_info[0] == "commentaire":
            self.delete_comment()
        
        else:
            self.send_error(405)
   
    #
    # On envoie le document statique demandé
    #
    def send_static(self):

        # on modifie le chemin d'accès en insérant un répertoire préfixe
        self.path = self.static_dir + self.path

        # on appelle la méthode parent (do_GET ou do_HEAD)
        # à partir du verbe HTTP (GET ou HEAD)
        if (self.command=='HEAD'):
            http.server.SimpleHTTPRequestHandler.do_HEAD(self)
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)

        # # solution alternative plus élégante :
            # method = 'do_{}'.format(self.command)
            # getattr(http.server.SimpleHTTPRequestHandler,method)(self)

    def send_commentaires_json(self):
        volcan = self.path_info[1]
        c = conn.cursor()
        c.execute('SELECT * FROM commentaires WHERE site = "{}" '.format(volcan))
        data = c.fetchall()
        # if len(data) == 0 :
            
        # on construit la réponse en json
        body = json.dumps([dict(d) for d in data])
        print([dict(d) for d in data])
        # on envoie la réponse au client
        headers = [('Content-Type','application/json')]
        self.send(body,headers)
  
    #
    # On envoie un document avec l'heure
    #
    def send_time(self):

        # on récupère l'heure
        t = self.date_time_string()
        
        # on génère un document au format html
        body = '<!doctype html>' + \
            '<meta charset="utf-8">' + \
           '<title>l\'heure</title>' + \
           '<div>Voici l\'heure du serveur :</div>' + \
           '<pre>{}</pre>'.format(t)

        # pour prévenir qu'il s'agit d'une ressource au format html
        headers = [('Content-Type','text/html;charset=utf-8')]

        # on envoie
        self.send(body,headers)


    # 
    # On envoie la liste des entités
    #
    def send_list(self):

        # on effectue une requête dans la base pour récupérer la liste des entités
        c = conn.cursor()
        c.execute("SELECT name, lat, lon FROM {}".format(entity_list_name))
        data = c.fetchall()
        
        # on construit la réponse en json
        body = json.dumps([dict(d) for d in data])
        
        # on envoie la réponse au client
        headers = [('Content-Type','application/json')]
        self.send(body,headers)


    #
    # On envoie les infos d'une entité
    #
    def send_data(self, name):
        
        # requête dans la base pour récupérer les infos de l'entité
        c = conn.cursor()
        c.execute("SELECT * FROM {} WHERE name=?".format(entity_list_name),(name,))
        r = c.fetchone()

        # construction de la réponse
        if r == None:
            self.send_error(404,'{} {} non trouvée'.format(entity_name,name))

        #  on a trouvé l'item recherché
        else :
            info = { 'other': {} }

            # rangement des informations reçues
            for k in r.keys():
                if k == 'wiki' or k == 'photo' or k == 'abstract' :
                    info[k] = r[k]
                elif '{}'.format(r[k]).startswith('http'):
                    info['dbpedia'] = r[k]
                elif not k == 'name':
                    info['other'][k] = r[k]
            
        # envoi de la réponse
        self.send_json(info)


    #
    # On envoie un document au format json
    #
    def send_json(self,data):
        headers = [('Content-Type','application/json')]
        self.send(json.dumps(data),headers)
        

    #
    # On envoie les entêtes et le corps fourni
    #
  
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

   
    #
    # On post un commentaire
    #
    def post_comment(self):
 
        # On récupère les données
        data = self.params
          
        # On vérifie que les données fournie correspondent bien à la requête
        try :
            pseudo = data['pseudo']
            password = data['password']
            site_name = data['site']
            message = data['message']
            date = data['date']
            timestamp = get_timestamp()
            
        except :
            self.send_error(422, "Format du corps invalide",
                         'Must provide a valid JSON body for the query POST "/commentaire" (Must contain : pseudo, password, site, message, date).')
            return
            
        none_empty_field = self.is_not_empty(pseudo)
        none_empty_field = none_empty_field and self.is_not_empty(password)
        none_empty_field = none_empty_field and self.is_not_empty(message)
        # la date est facultative
        
        if self.verify_connection(pseudo,password) and none_empty_field :
            c = conn.cursor()
            try :
                sql = 'INSERT INTO commentaires (pseudo,site,message,date,timestamp) VALUES ("{}","{}","{}","{}",{})'.format(pseudo,site_name,message,date,timestamp)
                c.execute(sql)
                conn.commit()
                # on indique que la commande s'est bien effectuée (send_response ne fonctionne pas mais le status reste le bon)
                self.send_json({'Status':'Done'}) 
            except:
                self.send_error(400,'Une erreur sql est survenue')


    def post_register(self):
 
        # On récupère les données
        data = self.params
          
        # On vérifie que les données fournie correspondent bien à la requête
        try :
            pseudo = data['user_pseudo']
            password = data['user_password']
            email = data['email']
            
        except :
            self.send_error(422, "Format du corps invalide",
                         'Must provide a valid JSON body for the query POST "/register" (Must contain : pseudo, password, email).')
            return
        
        none_empty_field = self.is_not_empty(pseudo)
        none_empty_field = none_empty_field and self.is_not_empty(email)
        none_empty_field = none_empty_field and self.is_not_empty(password)
        # la date est facultative
        
        if self.is_nouvel_utilisateur(pseudo,email) and none_empty_field :
            c = conn.cursor()
            try :
                sql = "INSERT INTO users (pseudo,mdp,email) VALUES ('{}','{}','{}')".format(pseudo,password,email)
                c.execute(sql)
                conn.commit()
                # on indique que la commande s'est bien effectuée (send_response ne fonctionne pas mais le status reste le bon)
                self.send_json({'Status':'Done'}) 
            except:
                self.send_error(400,'Une erreur sql est survenue (1)')

    #
    # On supprime un commentaire
    #
    def delete_comment(self):
        
        data = self.params
        # On vérifie que les données fournie correspondent bien à la requête
        try :
            comment_id = self.path_info[1]
            pseudo = data['pseudo']
            password = data['password']
        except :
            self.send_error(422, "Format du corps invalide",
                         'Must provide a valid JSON body for the query DELETE "/commentaire" (Must contain  : pseudo, password).')
            return    
        
        none_empty_field = self.is_not_empty(pseudo)
        none_empty_field = none_empty_field and self.is_not_empty(password)
        # la date est facultative
        
        if self.verify_connection(pseudo,password) and none_empty_field and self.is_owned_by(comment_id,pseudo) :
            c = conn.cursor()
            try :
                sql = 'DELETE FROM commentaires WHERE id = {}'.format(comment_id)
                c.execute(sql)
                conn.commit()
                # on indique que la commande s'est bien effectuée (send_response ne fonctionne pas mais le status reste le bon)
                self.send_json({'Status':'Done'}) 
            except:
                self.send_error(400,'Une erreur sql est survenue')
                
        
    #
    # Fonction qui vérifie si un utilisateur existe
    #
    def verify_connection(self,pseudo,password):
        
        verified = True 
        
        c = conn.cursor()
        try :
            sql = 'SELECT * FROM users WHERE pseudo = "{}" AND mdp = "{}"'.format(pseudo,password)
            c.execute(sql)
            r = c.fetchone()
            if r != None : # si l'utilisateur existe
                
                if r['email'] == None :
                    verified = False
                    self.send_error(401,"Missing 'email'")
            else : # l'utilisateur n'existe peut-être pas
                verified = False
                sql = 'SELECT * FROM users WHERE pseudo = "{}"'.format(pseudo)
                c.execute(sql)
                r = c.fetchone()
                if r == None : # l'utilisateur n'existe pas
                    self.send_error(401,"Unknown user : Please register")
                else : #mdp incorrect
                    self.send_error(401,"Mot de passe incorrect")
        except :
            self.send_error(400,'Une erreur sql est survenue')
            verified = False #on arrête la méthode mère
    
        return(verified)
    
    
    #
    # Méthode qui vérifie si un commentaire existe et si il correspond bien au pseudo donné
    #
    def is_owned_by(self,comment_id,pseudo):
        
        owned = True    
        c = conn.cursor()
        try :
            # On commence par vérifier si le commentaire existe
            sql = 'SELECT * FROM commentaires WHERE id = {}'.format(comment_id)
            c.execute(sql)
            r = c.fetchone()
            if r == None : # le commentaire n'existe pas
                owned = False
                self.send_error(404,"This comment doesn't exist", "Aucun id ne correspond")
            else : # il existe
                sql = 'SELECT * FROM commentaires WHERE id = {} AND pseudo = "{}"'.format(comment_id,pseudo)
                c.execute(sql)
                r = c.fetchone()
                if r == None : # Le commentaire n'est pas celui de l'utilisateur
                    owned = False
                    self.send_error(401,"Not allowed", "Vous n'avez pas la permission pour supprimer ce commentaire, vous n'êtes pas son auteur")
        except :
            self.send_error(400,'Une erreur sql est survenue')
            owned = False #on arrête la méthode mère
        
        return(owned)
    
    def is_nouvel_utilisateur(self,pseudo,email):
        
        nouvel_utilisateur = True
        c = conn.cursor()
        try:
            
            sql = 'SELECT * FROM users WHERE pseudo="{}"'.format(pseudo)
            c.execute(sql)
            r = c.fetchone()
            
            if r != None: # le pseudo existe déjà
                nouvel_utilisateur = False
                self.send_error(401,"Pseudo déjà utilisé", "Ce pseudo existe déjà. Veuillez en choisir un autre") 
            else:
                sql = 'SELECT * FROM users WHERE email="{}"'.format(email)
                c.execute(sql)
                r = c.fetchone()
                if r != None: #l'adresse mail existe déjà
                   nouvel_utilisateur = False
                   self.send_error(401,"Adresse mail déjà utilisée", "Cette adresse-mail est déjà utilisée. Veuillez en choisir une autre")  
        except:
            print('Une erreur sql est survenue')
            nouvel_utilisateur = False
        
        return(nouvel_utilisateur)
    
    def is_not_empty(self,elt):
        if elt == '':
            self.send_error(400,"Veuillez remplir tous les champs")
            return(False)
        else :
            return(True)
    #
    # Lecture des paramètres de la requête
    # 
    
    def init_params(self):
        
        info = self.path.split('?',2)
        if self.headers['Content-Type'] == "application/json":
            content_len = int(self.headers['Content-Length'])
            post_body = self.rfile.read(content_len)
            self.params = json.loads(post_body)
        else : 
            self.params = "Content-Type is different from 'application/json' "
        self.path_info = [unquote_plus(v) for v in info[0].split('/')[1:]]


        print('path_info : {}'.format(self.path_info))
        print('params : {}'.format(self.params))

    

def get_timestamp():
    """
    Méthode qui retourne le timestamp à l'heure de son activation
    """
    presentDate = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(presentDate)
    return(timestamp)
        


if __name__ == "__main__":
    

    entity_list_name = "volcans"


    # on en déduit le nom des entités au singulier
    entity_name = entity_list_name[:-1]
    

    #
    # Connexion à la base de données
    # conn est une variable globale
    #
    dbname = '{}.db'.format(entity_list_name)
    conn = sqlite3.connect(dbname)
    
    # pour récupérer les résultats sous forme d'un dictionnaire
    conn.row_factory = sqlite3.Row
    
    #
    # Instanciation et lancement du serveur
    #
    httpd = socketserver.TCPServer(("", 8080), RequestHandler)
    httpd.serve_forever()
