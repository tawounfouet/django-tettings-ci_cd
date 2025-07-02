# Utilise une image Python officielle
FROM python:3.11-slim


# Définit les variables d'environnement pour éviter les problèmes de bufferisation
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers nécessaires
COPY requirements.txt /app/

# Installe les dépendances
# Use --no-cache-dir pour éviter de stocker les paquets dans le cache
RUN pip install --no-cache-dir -r requirements.txt

# Copie l'ensemble du projet
COPY . /app/

# Collecte les fichiers statiques
RUN python manage.py collectstatic --noinput

# Définit la commande de lancement
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "--bind", "0.0.0.0:8000"]