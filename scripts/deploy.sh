#!/bin/bash
set -e

# Variables d'environnement
APP_DIR="/home/$USER/django-lettings-app"
REPO_URL="https://github.com/tawounfouet/django-lettings-ci_cd.git"

echo "📂 Setting up application directory..."
mkdir -p $APP_DIR

# Clone ou mise à jour du repository
if [ -d "$APP_DIR/.git" ]; then
  echo "📥 Pulling latest changes..."
  cd $APP_DIR
  git fetch origin
  git reset --hard origin/main 2>/dev/null || git reset --hard origin/master
else
  echo "📥 Cloning repository..."
  git clone $REPO_URL $APP_DIR
  cd $APP_DIR
fi

echo "🐍 Setting up virtual environment..."
if [ ! -d "$APP_DIR/venv" ]; then
  python3 -m venv $APP_DIR/venv
fi

source $APP_DIR/venv/bin/activate

echo "📦 Installing/updating dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🔧 Setting up environment variables..."
cat > .env << EOF
SECRET_KEY='$SECRET_KEY'
DEBUG=$DEBUG
SENTRY_DSN='$SENTRY_DSN'
ALLOWED_HOSTS='$SSH_HOST,127.0.0.1,localhost'
EOF

echo "🔄 Running database migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "🧹 Cleaning up old files..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo "🔄 Restarting application services..."
# Arrêter les anciens processus gunicorn s'ils existent
pkill -f "gunicorn.*oc_lettings_site" || true

# Démarrer gunicorn en arrière-plan
echo "🚀 Starting Gunicorn server..."
nohup gunicorn oc_lettings_site.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120 \
  --access-logfile $APP_DIR/access.log \
  --error-logfile $APP_DIR/error.log \
  --daemon

# Attendre que le serveur démarre
sleep 5

echo "✅ Deployment completed successfully!"

# Health check avec retry
echo "🔍 Performing health checks..."
for i in {1..5}; do
  if curl -f http://localhost:8000 > /dev/null 2>&1; then
    echo "🟢 Health check $i/5 passed - Application is running"
    break
  elif [ $i -eq 5 ]; then
    echo "🔴 Health check failed after 5 attempts"
    # Logs pour debugging
    echo "📋 Application error logs:"
    tail -n 20 $APP_DIR/error.log 2>/dev/null || echo "No error logs found"
    echo "📋 Application access logs:"
    tail -n 10 $APP_DIR/access.log 2>/dev/null || echo "No access logs found"
    exit 1
  else
    echo "🟡 Health check $i/5 failed, retrying in 5 seconds..."
    sleep 5
  fi
done

echo "🌐 Application available at: http://$SSH_HOST:8000"
echo "📋 Logs available at:"
echo "   - Error log: $APP_DIR/error.log"
echo "   - Access log: $APP_DIR/access.log"