"""Modèle message pour les conversation"""

from datetime import date
from typing import Any, cast
from typing import Optional, cast
from src.models.database import db


class Channel(db.Model):
    "Modèle representant une discution"

    __tablename__ = "Channel"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Relation parent-enfant
    ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.id"), nullable=False)

    ticket = db.relationship('Ticket', remote_side=[id])

    # INCOMPLETE