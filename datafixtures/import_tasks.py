"""
Script pour importer les catégories et sous-catégories en base de données
à partir du fichier categories.json.
"""

import json

from src.models.task import Task
from src.models.database import db

TASKS_JSON = "datafixtures/json/task.json"


def import_tasks() -> None:
    with open(TASKS_JSON, encoding="utf-8") as fp:
        data = json.load(fp)

    for task in data:
        # Crée la catégorie principale
        parent = Task.find_by_title(task["title"])
        if not parent:
            parent = Task(title=task["title"], content=task["content"], status=False,deadline=task["deadline"], author_id=task["author"], parent_id=None)
            db.session.add(parent)
            db.session.flush()  # Force l'attribution de l'ID
        # Crée les sous-catégories
        for sub in task["subtasks"]:
            subtask = Task.find_by_title(sub["title"])
            if not subtask:
                subtask = Task(title=sub["title"], content=sub["content"], status=False,deadline=sub["deadline"], author_id=sub["author"], parent_id=parent.id)
                db.session.add(subtask)
    db.session.commit()
    print(f"{len(data)} tasks ajoutées.")