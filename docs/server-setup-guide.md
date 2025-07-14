# 🚀 Guide de Configuration du Serveur pour Déploiement

## 📋 Prérequis Serveur

### 1. **Configuration Utilisateur SSH**

Pour que le déploiement automatisé fonctionne, l'utilisateur SSH doit avoir les permissions appropriées :

```bash
# Sur le serveur distant, exécuter ces commandes :

# 1. Installer les dépendances nécessaires
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git curl

# 2. Créer un utilisateur pour le déploiement (optionnel)
sudo adduser django-deploy
sudo usermod -aG sudo django-deploy

# 3. Configurer SSH pour l'utilisateur
# Copier votre clé publique SSH :
ssh-copy-id -i ~/.ssh/id_rsa.pub django-deploy@YOUR_SERVER_IP
```

### 2. **Configuration des Variables d'Environnement GitHub**

Dans les Settings de votre repository GitHub, ajouter ces secrets :

| Variable | Description | Exemple |
|----------|-------------|---------|
| `SSH_HOST` | IP ou domaine du serveur | `203.0.113.42` |
| `SSH_USER` | Nom d'utilisateur SSH | `django-deploy` |
| `SSH_PRIVATE_KEY` | Clé privée SSH | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `SECRET_KEY` | Clé secrète Django | `django-insecure-xyz...` |
| `DEBUG` | Mode debug | `False` |
| `SENTRY_DSN` | URL Sentry (optionnel) | `https://...` |

## 🔧 Script de Configuration Serveur

Créez ce script sur votre serveur pour automatiser la configuration :

```bash
#!/bin/bash
# save as setup-server.sh

set -e

echo "🔧 Configuration du serveur pour Django Lettings..."

# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation des dépendances
sudo apt install -y python3 python3-venv python3-pip git curl nginx

# Configuration du firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 8000/tcp
sudo ufw --force enable

# Création du répertoire d'application
mkdir -p /home/$USER/django-lettings-app

echo "✅ Serveur configuré avec succès!"
echo "🔗 Vous pouvez maintenant déclencher un déploiement depuis GitHub Actions"
```

## 🌐 Configuration Nginx (Optionnel)

Pour utiliser un reverse proxy avec Nginx :

```nginx
# /etc/nginx/sites-available/django-lettings
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/django-deploy/django-lettings-app/staticfiles/;
    }
}
```

Activez la configuration :
```bash
sudo ln -s /etc/nginx/sites-available/django-lettings /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔍 Vérification Post-Déploiement

Après un déploiement réussi, vérifiez :

```bash
# 1. Vérifier que l'application fonctionne
curl http://localhost:8000

# 2. Vérifier les processus Gunicorn
ps aux | grep gunicorn

# 3. Vérifier les logs
tail -f /home/$USER/django-lettings-app/error.log
tail -f /home/$USER/django-lettings-app/access.log

# 4. Tester les endpoints principaux
curl http://localhost:8000/lettings/
curl http://localhost:8000/profiles/
```

## 🛠️ Dépannage

### **Problème : Permission denied**
```bash
# Vérifier les permissions SSH
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

### **Problème : Python not found**
```bash
# Installer Python 3
sudo apt install python3 python3-venv python3-pip
```

### **Problème : Gunicorn ne démarre pas**
```bash
# Vérifier les logs d'erreur
cat /home/$USER/django-lettings-app/error.log

# Vérifier les dépendances
cd /home/$USER/django-lettings-app
source venv/bin/activate
pip install gunicorn
```

### **Problème : Health check échoue**
```bash
# Vérifier le port 8000
netstat -tlnp | grep 8000

# Tester manuellement
curl -v http://localhost:8000
```

## 📊 Monitoring

Pour surveiller l'application en continu :

```bash
# Créer un script de monitoring
cat > /home/$USER/monitor-app.sh << 'EOF'
#!/bin/bash
while true; do
    if ! curl -f http://localhost:8000 > /dev/null 2>&1; then
        echo "$(date): Application down, restarting..."
        cd /home/$USER/django-lettings-app
        source venv/bin/activate
        pkill -f "gunicorn.*oc_lettings_site" || true
        nohup gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:8000 --workers 3 --daemon
    fi
    sleep 60
done
EOF

chmod +x /home/$USER/monitor-app.sh
```

---

**🎯 Votre serveur est maintenant prêt pour le déploiement automatique !**
