"""Modèle message pour les conversation"""

from datetime import date
from typing import Any, cast
from typing import Optional, cast
from src.models.database import db


class Message(db.Model):
    "Modèle representant les message lier a une discution"

    __tablename__ = "Message"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Relation parent-enfant
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    chanelle_id = db.Column(db.Integer, db.ForeignKey('Task.id'), nullable=True)

    parent = db.relationship('Channel', remote_side=[id], backref='subtasks')
    author = db.relationship("User", back_populates="task")

# INCOMPLETE