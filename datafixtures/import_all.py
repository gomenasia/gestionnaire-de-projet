"""
Script principal pour importer les tasks, utilisateurs et produits en une seule commande.
"""
from app import create_app
from datafixtures.import_tasks import import_tasks
from src.models.database import db

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print("Suppression et création des tables...")
        db.drop_all()
        db.create_all()
        print("Import des tasks...")
        import_tasks()
    print("Import global terminé.")
