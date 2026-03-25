"""
Configuration pour l'application Flask.
Approche classique Flask avec classes de configuration.
Support des fichiers .env pour les variables d'environnement.
"""
import os
from pathlib import Path
from typing import Type

# Répertoire de base du projet
BASE_DIR = Path(__file__).resolve().parent

def _get_database_uri() -> str:
    """Récupère et nettoie l'URI de la base de données."""
    db_url = os.environ.get("DATABASE_URL")
    
    # 1. Gestion de PostgreSQL (Spécifique à Railway/Heroku)
    # SQLAlchemy exige 'postgresql://' mais Railway fournit souvent 'postgres://'
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        return db_url

    # 2. Gestion de SQLite (Local)
    if not db_url:
        db_url = "sqlite:///instance/app.db"

    if db_url.startswith("sqlite:///") and not db_url.startswith("sqlite:////"):
        relative_path = db_url.replace("sqlite:///", "")
        absolute_path = (BASE_DIR / relative_path).resolve()
        # On s'assure que le dossier 'instance' existe pour éviter l'erreur "unable to open"
        absolute_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{absolute_path}"

    return db_url


class Config:
    """Configuration de base."""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "cle-secrete-dev-non-securisee"
    SQLALCHEMY_DATABASE_URI = _get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuration pour le développement."""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """Configuration pour la production."""
    DEBUG = False
    
    # On surcharge ici pour forcer la vérification de la clé en prod
    def __init__(self):
        secret = os.environ.get("SECRET_KEY")
        # Sur Railway, si tu n'as pas encore créé la variable, 
        # on met une valeur par défaut temporaire pour ne pas bloquer le build
        if not secret and os.environ.get("RAILWAY_STATIC_URL"):
             print("⚠️ WARNING: SECRET_KEY non définie sur Railway !")
        elif not secret:
            raise ValueError("SECRET_KEY doit être définie en production")
        self.SECRET_KEY = secret

# Dictionnaire de configuration
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}