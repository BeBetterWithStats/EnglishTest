# PythonCode

## :movie_camera: Youtube
Utilitaire permettant de télécharger la vidéo Youtube dont l'url a été passée en paramètre de la ligne de commande. Si le paramètre est absent, une invitation de commande `input()` permettra à l'utilisateur de saisir l'URL de la vidéo.

### Comment lancer le programme
```$ python3 youtube.py <OPT url_video_youtube>```

### Liste des tâches à traiter
- [ ] Rendre le répertoire de destination paramétrable
- [ ] Ajouter un ficher de compte rendu du téléchargement (URL, titre, auteur, date du téléchargement)

## :chart_with_upwards_trend: Stock Market
Utilitaire permettant de consolider dans un seul fichier l'ensemble des opérations d'ordre de bourse (Achat / Vente) passées chez différents brokers.

Les plate-formes gérées sont :
- Revolut
- Degiro
- Trading 212

### Comment lancer le programme
```$ python3 stockmarket.py```

Vous pourrez sélectionner une des deux fonctionnalités actuellement implémentées :
1. Consolider l'ensemble des ordres d'achat et vente dans un seul fichier (qui sera nommé `allstockmarketorders.csv`)
2. Consolider l'ensemble des dividendes perçus dans un seul fichier (qui sera nommé `alldividends.csv`)

### Comment récupérer la liste des opérations pour chaque broker


### Liste des tâches à traiter
- [ ] Rendre le répertoire contenant les fichiers des brokers paramétrable
- [ ] Ajouter un compte rendu de l'importation des fichiers (nb d'opérations retenues, nb d'opérations exclues)
- [ ] Revoir la méthode de recherche du nom du brocker lors du parcours des fichiers