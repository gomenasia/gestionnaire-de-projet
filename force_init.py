# force_init.py
import os
import sys

# Ajouter le dossier courant au chemin de recherche Python
sys.path.append(os.getcwd())

try:
    from app import create_app
    from src.models.database import db
    print("✅ Imports réussis")
except ImportError as e:
    print(f"❌ Erreur d'import : {e}")
    sys.exit(1)

# On force l'environnement de production
os.environ["FLASK_CONFIG"] = "production"

app = create_app()

with app.app_context():
    print("⏳ Connexion à PostgreSQL Railway et création des tables...")
    try:
        db.create_all()
        print("🚀 SUCCÈS : Les tables ont été créées sur PostgreSQL Railway !")
    except Exception as e:
        print(f"💥 Erreur lors de la création : {e}")