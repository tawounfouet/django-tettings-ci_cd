# Guide de Dépannage - Déploiement Django Lettings CI/CD

## Problèmes d'Authentification GitHub

### Erreur : Permission denied (publickey)

**Symptôme :**
```
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```

**Solutions :**

#### Solution 1 : Utilisation HTTPS (Recommandée)
Cette solution utilise HTTPS au lieu de SSH pour cloner le repository, évitant les problèmes de clés SSH sur le serveur.

**Configuration automatique :** Le workflow a été modifié pour utiliser HTTPS automatiquement.

#### Solution 2 : Configuration des clés SSH sur le serveur
Si vous préférez utiliser SSH :

1. **Générer une clé SSH sur votre serveur :**
```bash
ssh-keygen -t ed25519 -C "server@yourserver.com"
```

2. **Ajouter la clé publique à GitHub :**
   - Copiez le contenu de `~/.ssh/id_ed25519.pub`
   - Allez dans GitHub Settings > SSH and GPG keys
   - Ajoutez la clé publique

3. **Modifier le workflow pour utiliser SSH :**
```yaml
REPO_URL="git@github.com:tawounfouet/django-lettings-ci_cd.git"
```

## Problèmes de Connexion SSH

### Erreur : Connection refused

**Vérifications :**
1. Le serveur est démarré et accessible
2. Le port SSH (22) est ouvert
3. Les credentials SSH sont corrects

```bash
# Test de connexion SSH
ssh -v user@server-ip
```

### Erreur : Host key verification failed

**Solution :**
```bash
# Sur votre machine locale
ssh-keyscan -H your-server-ip >> ~/.ssh/known_hosts
```

## Problèmes de Déploiement

### Erreur : Database migration failed

**Solutions :**
1. **Vérifier les permissions de la base de données**
2. **Exécuter les migrations manuellement :**
```bash
ssh user@server
cd /home/user/django-lettings-app
source venv/bin/activate
python manage.py migrate --noinput
```

### Erreur : Static files collection failed

**Solutions :**
1. **Vérifier les permissions du répertoire static**
2. **Collecte manuelle :**
```bash
python manage.py collectstatic --noinput --clear
```

### Erreur : Gunicorn startup failed

**Diagnostic :**
```bash
# Vérifier les logs
tail -f /home/user/django-lettings-app/error.log

# Test manuel de Gunicorn
cd /home/user/django-lettings-app
source venv/bin/activate
gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:8000
```

## Problèmes de Configuration

### Variables d'environnement manquantes

**Vérification :**
```bash
# Sur le serveur
cat /home/user/django-lettings-app/.env
```

**Variables requises :**
- SECRET_KEY
- DEBUG
- SENTRY_DSN
- ALLOWED_HOSTS

### Problèmes de permissions

**Solutions :**
```bash
# Corriger les permissions
sudo chown -R user:user /home/user/django-lettings-app
chmod -R 755 /home/user/django-lettings-app
```

## Tests de Diagnostic

### Test de connectivité SSH
```bash
ssh -o ConnectTimeout=10 user@server-ip "echo 'SSH connection successful'"
```

### Test de l'application
```bash
curl -I http://server-ip:8000
```

### Vérification des processus
```bash
# Sur le serveur
ps aux | grep gunicorn
netstat -tulpn | grep :8000
```

## Commandes Utiles de Dépannage

### Redémarrage complet de l'application
```bash
ssh user@server << 'EOF'
cd /home/user/django-lettings-app
pkill -f "gunicorn.*oc_lettings_site" || true
source venv/bin/activate
nohup gunicorn oc_lettings_site.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120 \
  --access-logfile access.log \
  --error-logfile error.log \
  --daemon
EOF
```

### Nettoyage des anciens déploiements
```bash
# Sur le serveur
cd /home/user/django-lettings-app
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
```

### Surveillance des logs en temps réel
```bash
# Sur le serveur
tail -f /home/user/django-lettings-app/error.log
tail -f /home/user/django-lettings-app/access.log
```

## Checklist de Dépannage

### Avant le déploiement
- [ ] Secrets GitHub configurés
- [ ] Serveur accessible via SSH
- [ ] Python 3.11+ installé sur le serveur
- [ ] Git installé sur le serveur

### Pendant le déploiement
- [ ] Étape build réussie
- [ ] Tests passés avec succès
- [ ] Connexion SSH établie
- [ ] Repository cloné/mis à jour
- [ ] Dépendances installées
- [ ] Migrations exécutées
- [ ] Fichiers statiques collectés
- [ ] Gunicorn démarré

### Après le déploiement
- [ ] Application accessible sur le port 8000
- [ ] Health check réussi
- [ ] Logs sans erreurs critiques

## Contacts et Support

En cas de problème persistant :
1. Vérifiez les logs GitHub Actions
2. Consultez les logs du serveur
3. Testez manuellement chaque étape sur le serveur
4. Référez-vous à la documentation Django et Gunicorn

## Ressources Additionnelles

- [Documentation Django Deployment](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Guide Gunicorn](https://docs.gunicorn.org/en/stable/deploy.html)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
