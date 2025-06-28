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



## Étape 1 : Améliorez l’architecture modulaire de votre projet

Nous optimisons notre architecture de site web en réduisant les problèmes de notre
conception monolithique actuelle. Nous allons :
- réorganiser notre code en plusieurs applications distinctes ;
- déplacer les fichiers HTML du site dans des dossiers de templates spécifiques
à chaque application.
Cette optimisation améliorera la flexibilité, la maintenabilité et l'évolutivité de notre
code.

### Aspects techniques
Nous prévoyons de séparer `oc_lettings_site` en deux applications distinctes: 
- "lettings"
- "profiles", 
  
Pour améliorer la modularité, l'extensibilité et la séparation des
fonctionnalités. Voici les modifications à effectuer pour cette optimisation :
- créer une nouvelle application "lettings", contenant les modèles "Address" et
"Letting" ;
- remplir les nouvelles tables avec les données déjà présentes dans la base de
données en utilisant les fichiers de migration Django. Attention, il ne faut pas
utiliser le langage SQL directement dans le fichier de migration ;
- créer une nouvelle application "profiles", contenant le modèle "Profile" ;
- répéter l’opération de migration pour cette nouvelle application ;
- en utilisant les migrations Django, supprimer les anciennes tables de la base de
données ;
- remplacer les templates de manière cohérente dans les nouvelles applications ;


#### Créer les applications lettings et profiles

```bash
source .venv/bin/activate
# Créer les applications lettings et profiles
python3 manage.py startapp lettings
python3 manage.py startapp profiles

# ajouter les applications dans le fichier settings.py
# settings.py
INSTALLED_APPS = [
    ...
    'lettings',
    'profiles',
    ...
]
```


####  Créer les modèles Letting et Profile
```python
# lettings/models.py
from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    def __str__(self):
        return f'{self.number} {self.street}'


class Letting(models.Model):
    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# profiles/models.py
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.user.username
```

#### Générer les fichiers de migration pour lettings et profiles
 
```bash
python3 manage.py makemigrations oc_lettings_site lettings profiles


# sortie du terminal
Migrations for 'lettings':
  lettings/migrations/0001_initial.py
    - Create model Address
    - Create model Letting
Migrations for 'oc_lettings_site':
  oc_lettings_site/migrations/0002_auto_20240315_1806.py
    - Remove field address from letting
    - Remove field user from profile
    - Delete model Address
    - Delete model Letting
    - Delete model Profile
Migrations for 'profiles':
  profiles/migrations/0001_initial.py
    - Create model Profile
```

#### Remplir les nouvelles tables avec les données déjà présentes dans la base de données en utilisant les fichiers de migration Django.

```bash
python3 manage.py sqlmigrate lettings 0001
#python3 manage.py migrate lettings

# sortie du terminal
BEGIN;
--
-- Create model Address
--
CREATE TABLE "lettings_address" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "number" integer unsigned NOT NULL CHECK ("number" >= 0), "street" varchar(64) NOT NULL, "city" varchar(64) NOT NULL, "state" varchar(2) NOT NULL, "zip_code" integer unsigned NOT NULL CHECK ("zip_code" >= 0), "country_iso_code" varchar(3) NOT NULL);
--
-- Create model Letting
--
CREATE TABLE "lettings_letting" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(256) NOT NULL, "address_id" integer NOT NULL UNIQUE REFERENCES "lettings_address" ("id") DEFERRABLE INITIALLY DEFERRED);
COMMIT;
```

**Rename the Old Table**
Now that you have the name Django generated for the model, you’re ready to rename the old table. To drop the Letting model from the oc_lettings_site app, Django created two migrations:

- 0001_initial.py, which created the Letting model
- 0002_auto_20240315_1639.py, which deleted the Letting model


before
```python
    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Letting',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
```



```python
# oc_lettings_site/migrations/0002_auto_20240315_1639.py

 class Migration(migrations.Migration):

    dependencies = [
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='profile',
                    name='user',
                ),
            ],
            database_operations=[],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Letting',
                ),
            ],
            database_operations=[],
        ),


        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Profile',
                ),
            ],
            database_operations=[],
        ),
    ]
# Generated by Django 3.0 on 2024-03-15 16:39
```


```python
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Address',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('number', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999)])),
                        ('street', models.CharField(max_length=64)),
                        ('city', models.CharField(max_length=64)),
                        ('state', models.CharField(max_length=2, validators=[django.core.validators.MinLengthValidator(2)])),
                        ('zip_code', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99999)])),
                        ('country_iso_code', models.CharField(max_length=3, validators=[django.core.validators.MinLengthValidator(3)])),
                    ],
                ),
            ],
            database_operations=[],
            ),
        
            
        migrations.SeparateDatabaseAndState(
            state_operations=[       
                migrations.CreateModel(
                    name='Letting',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('title', models.CharField(max_length=256)),
                        ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lettings.Address')),
                    ],
                ),
            ],
            database_operations=[],
        ),
    ]
```

```bash
#show migrations
python3 manage.py showmigrations

# back to the previous migration
oc_lettings_site
 [X] 0001_initial
python3 manage.py migrate oc_lettings_site 0001
```

```python
class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999)])),
                ('street', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=2, validators=[django.core.validators.MinLengthValidator(2)])),
                ('zip_code', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99999)])),
                ('country_iso_code', models.CharField(max_length=3, validators=[django.core.validators.MinLengthValidator(3)])),
            ],
        ),
        
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite_city', models.CharField(blank=True, max_length=64)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Letting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='oc_lettings_site.Address')),
            ],
        ),
    ]
```

apres
```python
class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Address',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('number', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999)])),
                        ('street', models.CharField(max_length=64)),
                        ('city', models.CharField(max_length=64)),
                        ('state', models.CharField(max_length=2, validators=[django.core.validators.MinLengthValidator(2)])),
                        ('zip_code', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99999)])),
                        ('country_iso_code', models.CharField(max_length=3, validators=[django.core.validators.MinLengthValidator(3)])),
                    ],
                ),
            ],
            database_operations=[],
            ),

        migrations.SeparateDatabaseAndState(
            state_operations=[  
                migrations.CreateModel(
                    name='Profile',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('favorite_city', models.CharField(blank=True, max_length=64)),
                        ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                    ],
                ),
            ],
            database_operations=[],
        ),

        migrations.SeparateDatabaseAndState(
            state_operations=[       
                migrations.CreateModel(
                    name='Letting',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('title', models.CharField(max_length=256)),
                        ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lettings.Address')),
                    ],
                ),
            ],
            database_operations=[],
        ),
    ]
    
```