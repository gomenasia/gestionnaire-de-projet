"""Modèle message pour les conversation"""

from src.utils import get_utc_now
from src.models.database import db


class Message(db.Model):
    "Modèle representant les message lier a une discution"

    __tablename__ = "Message"

    id         = db.Column(db.Integer, primary_key=True)
    content    = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=get_utc_now())

    # Clés étrangères
    author_id  = db.Column(db.Integer, db.ForeignKey("user.id"),    nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False)

    # Relations
    author  = db.relationship("User",    back_populates="messages")
    channel = db.relationship("Channel", back_populates="messages")

# INCOMPLETE