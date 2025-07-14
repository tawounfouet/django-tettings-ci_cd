# Configuration du Workflow de Déploiement - Django Lettings CI/CD

## Overview

Ce fichier documente la configuration du workflow GitHub Actions pour le déploiement automatique de l'application Django Lettings vers un serveur cloud.

## Fichier de Workflow

**Emplacement :** `.github/workflows/deploy-to-cloud.yml`

## Déclencheurs (Triggers)

Le workflow se déclenche dans les cas suivants :

```yaml
on:
  push:
    branches: [ 'main', 'master' ]    # Push sur la branche principale
  pull_request:
    branches: [ 'main', 'master' ]    # Pull Request vers la branche principale
  workflow_dispatch:                  # Déclenchement manuel
```

## Jobs et Étapes

### 1. Job `build` - Construction et Linting

**Objectif :** Vérifier la qualité du code et installer les dépendances

**Étapes :**
- ✅ Checkout du code source
- ✅ Configuration de Python 3.11
- ✅ Cache des dépendances pip
- ✅ Installation des dépendances
- ✅ Linting avec flake8 (configuration adaptée au setup.cfg)

**Configuration spécifique Django Lettings :**
```yaml
# Adapté au setup.cfg du projet
flake8 . --max-line-length=99 --exclude=migrations,venv
```

### 2. Job `test` - Tests et Couverture

**Objectif :** Exécuter les tests et mesurer la couverture de code

**Étapes :**
- ✅ Installation des dépendances de test
- ✅ Migrations de base de données pour les tests
- ✅ Exécution des tests avec pytest-django
- ✅ Génération du rapport de couverture
- ✅ Upload optionnel vers Codecov

**Configuration spécifique :**
```yaml
DJANGO_SETTINGS_MODULE: oc_lettings_site.settings
# Tests avec pytest configuré dans setup.cfg
python -m pytest --cov=. --cov-report=term-missing
```

### 3. Job `security-scan` - Analyse de Sécurité

**Objectif :** Scanner les vulnérabilités de sécurité

**Outils utilisés :**
- **Safety :** Vérification des vulnérabilités dans les dépendances
- **Bandit :** Analyse statique de sécurité du code Python

### 4. Job `deploy` - Déploiement

**Objectif :** Déployer l'application sur le serveur cloud

**Conditions de déclenchement :**
- Tous les jobs précédents réussis
- Push sur branche main/master uniquement
- Environnement de production configuré

**Étapes détaillées :**

#### 4.1 Préparation
```yaml
- Extract commit info (hash, message, timestamp)
- Setup SSH connection
- Add server to known hosts
```

#### 4.2 Déploiement SSH
```bash
# Variables d'environnement
APP_DIR="/var/www/django-lettings-app"
REPO_URL="https://github.com/YOUR_USERNAME/django-lettings-ci_cd.git"

# Clone/Update repository
# Setup virtual environment
# Install dependencies
# Configure environment variables
# Run migrations
# Collect static files
# Restart services
# Health checks
```

#### 4.3 Variables d'environnement déployées
```bash
SECRET_KEY='$SECRET_KEY'
DEBUG=$DEBUG
SENTRY_DSN='$SENTRY_DSN'
ALLOWED_HOSTS='$SSH_HOST,127.0.0.1,localhost'
```

#### 4.4 Health Checks
- 5 tentatives avec délai de 5 secondes
- Vérification de `http://localhost:8000`
- Logs d'erreur en cas d'échec

### 5. Job `post-deployment` - Tâches Post-Déploiement

**Objectif :** Tâches de monitoring et notification

**Fonctionnalités :**
- Notifications de déploiement
- Monitoring de performance (optionnel)
- Mise à jour des badges de statut

## Secrets GitHub Requis

Pour que le déploiement fonctionne, vous devez configurer les secrets suivants dans votre repository GitHub :

### Secrets Requis

1. **SSH_HOST** - L'adresse IP ou nom d'hôte de votre serveur cloud
2. **SSH_USER** - Le nom d'utilisateur pour la connexion SSH  
3. **SSH_PRIVATE_KEY** - La clé privée SSH pour l'authentification
4. **SECRET_KEY** - La clé secrète Django pour la production
5. **DEBUG** - Définir à `False` pour la production
6. **SENTRY_DSN** - URL de configuration Sentry pour le monitoring
7. **GITHUB_TOKEN** - Token GitHub pour cloner le repository (automatiquement disponible)

### Configuration des Secrets

1. Allez dans votre repository GitHub
2. Cliquez sur **Settings** > **Secrets and variables** > **Actions**
3. Cliquez sur **New repository secret** pour chaque secret
4. Ajoutez les valeurs correspondantes

**Note :** Le `GITHUB_TOKEN` est automatiquement fourni par GitHub Actions et n'a pas besoin d'être configuré manuellement.

## Configuration du Serveur

### Prérequis serveur

```bash
# Installation des dépendances
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx supervisor git

# Création de l'utilisateur de déploiement (optionnel)
sudo useradd -m -s /bin/bash deploy
sudo usermod -aG sudo deploy
```

### Structure de déploiement

```
/var/www/django-lettings-app/
├── .git/                    # Repository Git
├── .env                     # Variables d'environnement
├── venv/                    # Environnement virtuel Python
├── manage.py               # Script de gestion Django
├── requirements.txt        # Dépendances Python
├── oc_lettings_site/      # Application principale
├── lettings/              # Application lettings
├── profiles/              # Application profiles
├── static/                # Fichiers statiques
└── staticfiles/           # Fichiers statiques collectés
```

### Configuration Nginx (exemple)

```nginx
# /etc/nginx/sites-available/django-lettings
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /var/www/django-lettings-app/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Configuration Supervisor (exemple)

```ini
# /etc/supervisor/conf.d/django-lettings.conf
[program:django-lettings]
command=/var/www/django-lettings-app/venv/bin/gunicorn oc_lettings_site.wsgi:application --bind 127.0.0.1:8000 --workers 3
directory=/var/www/django-lettings-app
user=deploy
autostart=true
autorestart=true
stdout_logfile=/var/log/django-lettings.log
stderr_logfile=/var/log/django-lettings-error.log
```

## Utilisation

### Déploiement automatique

1. **Push sur main/master :** Déclenche automatiquement le workflow complet
2. **Pull Request :** Exécute build, test et security-scan uniquement
3. **Déploiement manuel :** Via l'onglet Actions > Run workflow

### Monitoring du déploiement

1. Allez dans **Actions** dans votre repository GitHub
2. Sélectionnez le workflow "Deploy Django Lettings to Cloud"
3. Suivez les logs en temps réel

### Rollback en cas de problème

```bash
# Connexion SSH au serveur
ssh user@your-server

# Rollback Git
cd /var/www/django-lettings-app
git reset --hard HEAD~1  # Revenir au commit précédent

# Restart services
sudo supervisorctl restart django-lettings
sudo systemctl reload nginx
```

## Personnalisation

### Modifier l'URL du repository

```yaml
# Dans le workflow, ligne ~120
REPO_URL="https://github.com/YOUR_USERNAME/django-lettings-ci_cd.git"
```

### Ajouter des étapes personnalisées

```yaml
# Exemple : backup de base de données avant déploiement
- name: Backup database
  run: |
    ssh $SSH_USER@$SSH_HOST "cd $APP_DIR && python manage.py dbbackup"
```

### Configuration d'environnements multiples

```yaml
# Utiliser des environnements GitHub
environment: 
  name: production
  url: http://your-domain.com
```

## Troubleshooting

### Erreurs communes

1. **SSH Permission denied**
   - Vérifiez la clé SSH dans les secrets
   - Confirmez que la clé publique est sur le serveur

2. **Migration failed**
   - Vérifiez les permissions de la base de données
   - Confirmez que les migrations sont à jour

3. **Static files error**
   - Vérifiez les permissions du dossier staticfiles
   - Confirmez la configuration STATIC_ROOT

4. **Service restart failed**
   - Vérifiez que Supervisor/Systemd est configuré
   - Confirmez les permissions sudo pour l'utilisateur

### Logs utiles

```bash
# Logs de l'application
tail -f /var/log/django-lettings.log

# Logs Nginx
sudo tail -f /var/log/nginx/error.log

# Logs Supervisor
sudo supervisorctl tail -f django-lettings

# Status des services
sudo systemctl status nginx
sudo supervisorctl status
```

## Sécurité

### Bonnes pratiques

1. **Secrets :** Ne jamais exposer les clés dans le code
2. **SSH :** Utiliser des clés SSH dédiées pour le déploiement
3. **Permissions :** Utiliser un utilisateur dédié avec permissions minimales
4. **HTTPS :** Configurer SSL/TLS en production
5. **Firewall :** Limiter les ports ouverts sur le serveur

### Monitoring

- **Sentry :** Pour le monitoring des erreurs
- **Health checks :** Vérification automatique du bon fonctionnement
- **Logs centralisés :** Collecte et analyse des logs

## Performance

### Optimisations

1. **Cache pip :** Accélère l'installation des dépendances
2. **Parallel jobs :** Build, test et security-scan en parallèle
3. **Conditional deployment :** Déploie seulement sur main/master
4. **Static files :** Collecte optimisée avec `--clear`

### Métriques

- Temps de build : ~2-4 minutes
- Temps de test : ~1-3 minutes  
- Temps de déploiement : ~2-5 minutes
- **Total :** ~5-12 minutes selon la taille du projet

Ce workflow offre une solution complète de CI/CD pour l'application Django Lettings avec des fonctionnalités avancées de sécurité, monitoring et récupération d'erreurs.
