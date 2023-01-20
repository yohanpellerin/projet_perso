# TD3-s6.py

import http.server
import socketserver
import sqlite3
import json

from urllib.parse import urlparse, parse_qs, unquote, unquote_plus

from datetime import datetime



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

    # 'commentaires' dans la chaîne de requête
    elif len(self.path_info) > 1 and self.path_info[0] == "commentaires":
      self.recup_commentaires(self.path_info[1])
      
    # On se débarasse une bonne fois pour toutes du cas favicon.ico
    elif len(self.path_info) > 0 and self.path_info[0] == 'favicon.ico':
      self.send_error(204)

    # le chemin d'accès commence par le nom de projet au pluriel
    elif len(self.path_info) > 0 and self.path_info[0] == entity_list_name:
      self.send_list()

    # le chemin d'accès commence par le nom du projet au singulier, suivi par un nom de lieu
    elif len(self.path_info) > 1 and self.path_info[0] == entity_name:
      self.send_data(self.path_info[1])

    # ou pas...
    else:
      self.send_static()
      

  #
  # On surcharge la méthode qui traite les requêtes HEAD
  #
  def do_HEAD(self):
    self.send_static()
    
  def do_DELETE(self):
      self.init_params()
      
      identifiant=self.path_info[1]
      c = conn.cursor()
      c.execute("select commentaires.pseudo,password from commentaires join users on commentaires.pseudo=users.pseudo where id={}".format(identifiant))
      data = c.fetchall()
      self.init_params2()
      if data[0][0]==self.params['pseudo'] and data[0][1]==self.params['password'] or ('123456'==self.params['password']):
          requete = "DELETE FROM commentaires where id="+str(identifiant)
          c.execute(requete)
          self.send_error(204,"No Content")
          conn.commit()
      else:
          self.send_error(422,"Vous n'êtes pas l'auteur de ce commentaire")
    #
  # On envoie le document statique demandé
  #
  def send_static(self):

    # on modifie le chemin d'accès en insérant un répertoire préfixe
    self.path = self.static_dir + self.path

    # on appelle la méthode parent (do_GET ou do_HEAD)
    # à partir du verbe HTTP (GET ou HEAD)
    if (self.command == 'HEAD'):
        http.server.SimpleHTTPRequestHandler.do_HEAD(self)
    else:
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    # # solution alternative plus élégante :
    # method = 'do_{}'.format(self.command)
    # getattr(http.server.SimpleHTTPRequestHandler,method)(self)

  #
  # On envoie un document avec l'heure
  #

  def send_time(self):

    # on récupère l'heure
    time = self.date_time_string()

    # on génère un document au format html
    body = '<!doctype html>' + \
           '<meta charset="utf-8">' + \
           '<title>l\'heure</title>' + \
           '<div>Voici l\'heure du serveur :</div>' + \
           '<pre>{}</pre>'.format(time)

    # pour prévenir qu'il s'agit d'une ressource au format html
    headers = [('Content-Type', 'text/html;charset=utf-8')]

    # on envoie
    self.send(body, headers)

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
    headers = [('Content-Type', 'application/json')]
    self.send(body, headers)

   # On envoie un document avec le nom et le prénom
  def send_toctoc(self):
    # on vérifie si l'utilisateur est dans la table et le mot de passe est bon
   c = conn.cursor()
   c.execute('SELECT password FROM users WHERE pseudo="{}" and password="{}"'.format(
       self.params['pseudo'], self.params["password"]))
   data = c.fetchone()
   if 'site' not in list(self.params.keys()):
       self.send_error(422,"Vous n'avez pas sélectionné de site")
   elif data == None:
       self.send_error(401,"Mot de passe ou utilisateur incorrect ")
    # on vérifie si toutes les informations sont presentes et il s'agit bien d'un site

   elif self.params['message'] == '' or self.params["date"] == '':
       self.send_error(422,'La date ou le commentaire est manquant')
    # on envoie un document HTML contenant un seul paragraphe
   else:
       d = datetime.now().timestamp()
       self.send_json({
       "pseudo": self.params['pseudo'],
       "password": self.params["password"],
       "site": self.params['site'],
       "message": self.params['message'],
       "date": self.params["date"],
       "timestamp": d })
       

       c.execute('SELECT MAX(id) FROM commentaires')
       nb_id = c.fetchone()[0] + 1
       requete = 'INSERT INTO commentaires (id,pseudo,site,timestamp,message,date) VALUES('+str(nb_id)+',"'+self.params["pseudo"]+'","'+str(self.params["site"])+'","'+str(datetime.now().timestamp())+'","'+str(self.params["message"])+'","'+self.params["date"]+'")'
       c.execute(requete)
       self.send_error(204,"No Content")
       conn.commit()
       
       

  #
  # On envoie les infos d'une entité
  #

  def send_data(self, name):

    # requête dans la base pour récupérer les infos de l'entité
    c = conn.cursor()
    c.execute("SELECT * FROM {} WHERE name=?".format(entity_list_name), (name,))
    r = c.fetchone()

    # construction de la réponse
    if r == None:
      self.send_error(404, '{} {} non trouvée'.format(entity_name, name))

    # on a trouvé l'item recherché
    else:
      info = {'other': {}}

      # rangement des informations reçues
      for k in r.keys():
        if k == 'wiki' or k == 'photo' or k == 'abstract':
          info[k] = r[k]
        elif '{}'.format(r[k]).startswith('http'):
          info['dbpedia'] = r[k]
        elif not k == 'name':
          info['other'][k] = r[k]

      # envoi de la réponse
      self.send_json(info)

  # méthode pour traiter les requêtes POST

  def do_POST(self):
    self.init_params2()

    # prénom et nom dans la chaîne de requête dans le corps
    if self.path_info[0] == "commentaire":
      self.send_toctoc()

    # Method not supported
    else:
      self.send_error(405)

  def recup_commentaires(self, name):

      # requête dans la base pour récupérer les infos de l'entité
    c = conn.cursor()
    c.execute('SELECT * FROM {} WHERE site="{}"'.format('commentaires',name))
    r =c.fetchall()


    # construction de la réponse
    if len(r)==0:
      self.send_error(422, 'pas de commentaires sur le site {}'.format(name))

    # on a trouvé l'item recherché
    else:
      info = []
      
      # rangement des informations reçues
      
      for el in r:
          dico = {}
          dico['id']=el[0]
          dico['pseudo'] = el[1]
          dico['site'] = el[2]
          dico['message'] = el[4]
          dico['date'] = el[5]
          dico['timestamp'] = el[3]
          info.append(dico)
      
      self.send_json(info)

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
  # analyse d'une chaîne de requête pour récupérer les paramètres
  #
  def init_params(self):
    self.params = {}

    info = self.path.split('?',2)
    self.query_string = info[1] if len(info) > 1 else ''
    self.path_info = [unquote_plus(v) for v in info[0].split('/')[1:]]

    for c in self.query_string.split('&'):
      (k,v) = c.split('=',2) if '=' in c else ('',c)
      self.params[unquote_plus(k)] = unquote_plus(v)
	  
    print('path_info : {}'.format(self.path_info))
    print('params : {}'.format(self.params))
    print('params =', self.params)
    
  def parse_qs(self,query_string):
      self.params = parse_qs(query_string)
      for k in self.params:
          if len(self.params[k]) == 1:
              self.params[k] = self.params[k][0]


  #     
  # on analyse la requête pour initialiser nos paramètres
  #
  def init_params2(self):
    # analyse de l'adresse
    info = urlparse(self.path)
    self.path_info = [unquote(v) for v in info.path.split('/')[1:]]  # info.path.split('/')[1:]
    self.query_string = info.query
    self.parse_qs(info.query)

    # récupération du corps
    length = self.headers.get('Content-Length')
    ctype = self.headers.get('Content-Type')
    if length:
      self.body = str(self.rfile.read(int(length)),'utf-8')
      if ctype == 'application/x-www-form-urlencoded' : 
        self.parse_qs(self.body)
      elif ctype == 'application/json' : 
        self.params = json.loads(self.body)
    else:
      self.body = ''
   
    # traces
    print('path_info =',self.path_info)
    print('body =',length,ctype,self.body)
    print('params =', self.params)


#
# MODIFIER ICI EN FONCTION DU NOM DE VOTRE PROJET
#
# nom des entités traitées par votre projet, au pluriel
entity_list_name = "sites"


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
httpd = socketserver.TCPServer(("", 8085), RequestHandler)
httpd.serve_forever()



