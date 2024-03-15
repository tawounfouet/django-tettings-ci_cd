## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /django-tettings-ci_cd/`
- `python3.10 -m venv .venv`
- `source .venv/bin/activate`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python3 --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /django-tettings-ci_cd/`
- `source .venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python3 manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /django-tettings-ci_cd/`
- `source .venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /django-tettings-ci_cd/`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
```bash
sqlite3 oc-lettings-site.sqlite3
sqlite> .tables
sqlite> pragma table_info(Python-OC-Lettings-FR_profile);
sqlite> select user_id, favorite_city from Python-OC-Lettings-FR_profile where favorite_city like 'B%';
```

- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`


## Configuration Read the Docs / Sphinx

1. Configuration de l’environnement :
Installez Sphinx en utilisant la commande pip install sphinx dans le
répertoire de votre projet.
```bash
source .venv/bin/activate
pip install sphinx
```

3. Initialisation du projet de documentation :
- Créez un répertoire doc pour votre projet de documentation ;
- Accédez au répertoire et exécutez la commande sphinx-quickstart ;
- Répondez aux questions pour configurer le projet, y compris le thème, le
format de sortie, etc. Vous pouvez choisir les options par défaut pour
commencer.
```bash
mkdir doc
cd doc
sphinx-quickstart
```


Vous devez maintenant compléter votre fichier principal `/django-tettings-ci_cd/doc/source/index.rst` et créer d'autres fichiers sources de documentation. Utilisez le Makefile pour construire la documentation comme ceci :
   make builder
où « builder » est l'un des constructeurs disponibles, tel que html, latex, ou linkcheck.
```bash
make html
```

3. Édition de la documentation :
Dans le répertoire de votre projet et dans le dossier source dans lequel
vous trouverez un fichier index.rst. C'est le point d'entrée de votre
documentation ;
- Éditez ce fichier en utilisant la syntaxe reStructuredText pour ajouter
votre contenu, sections, titres, etc. ;
- Vous pouvez créer des fichiers séparés pour les différentes parties de
votre documentation et les inclure dans le fichier index.rst en utilisant la
directive `.. include`.


4. Personnalisation du thème :
Si vous souhaitez personnaliser l'apparence de votre documentation,
vous pouvez modifier le fichier de configuration `conf.py` qui se trouve
dans le dossier source pour spécifier un thème personnalisé ou ajuster
les options du thème par défaut.