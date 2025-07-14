"""
Settings de test pour Django Lettings
Contourne les problèmes de migration pour les tests CI/CD
"""

from .settings import *

# Base de données en mémoire pour les tests rapides
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}


# Désactiver les migrations problématiques pour les tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


# Utiliser seulement les migrations initiales pour les tests
# Ignorer les migrations de renommage qui causent des problèmes
MIGRATION_MODULES = {
    "lettings": None,
    "profiles": None,
    "oc_lettings_site": None,
    "admin": None,
    "auth": None,
    "contenttypes": None,
    "sessions": None,
}

# Configuration spécifique aux tests
SECRET_KEY = "django-test-secret-key-very-long-and-secure-for-ci-testing"
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]

# Désactiver les logs pendant les tests
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "handlers": ["null"],
    },
}

# Pas de cache pendant les tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Désactiver Sentry pour les tests
SENTRY_DSN = None

# Pas de fichiers statiques pendant les tests
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
