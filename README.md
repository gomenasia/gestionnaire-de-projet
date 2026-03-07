# Gestionnaire de Tickets

Application web Flask pour gérer des tickets, des tâches et une messagerie temps réel.

## Fonctionnalités principales

- Authentification: inscription, connexion, déconnexion.
- Tickets: création, édition par l'auteur, gestion admin (statut + réponse).
- Profils utilisateurs: informations, statistiques, changement de mot de passe.
- Planning: gestion des tâches et sous-tâches.
- Chat temps réel par canal via `Flask-SocketIO`.

## Prérequis

- Python 3.10+
- `pip`

## Installation

```bash
python -m venv .venv
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

Puis:

```bash
pip install -r requirements.txt
```

## Lancer l'application

Mode développement (recommandé):

```bash
python app.py
```

Alternative:

```bash
python run.py development
```

Application disponible sur `http://127.0.0.1:5000`.

## Base de données

La base est initialisée automatiquement au démarrage.  
Commande disponible:

```bash
flask --app app init-db
```

## Import des données fixtures

```bash
python -m datafixtures.import_all
```

## Tests

```bash
pytest
```

## Lancement production

```bash
python run.py production
```
