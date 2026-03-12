"""Modèle message pour les conversation"""

from src.utils import get_utc_now
from sqlalchemy import func
from typing import cast
from src.models.database import db


class Message(db.Model):
    "Modèle representant les message lier a une discution"

    __tablename__ = "Message"

    id         = db.Column(db.Integer, primary_key=True)
    content    = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=get_utc_now)

    # Clés étrangères
    author_id  = db.Column(db.Integer, db.ForeignKey("User.id"),    nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("Channel.id"), nullable=False)

    # Relations
    author  = db.relationship("User",    back_populates="messages")
    channel = db.relationship("Channel", back_populates="messages")

    read_statuses = db.relationship('MessageReadStatus', backref='message', lazy='dynamic')

    @classmethod
    def find_by_id(cls, message_id: int) -> "Message | None":
        """Retourne un message par son id ou None s'il n'existe pas."""
        return cast("Message | None", cls.query.get(message_id))
    
    @classmethod
    def find_by_channel_id(cls, channel_id: int) -> list["Message"]:
        """Retourne un channel par son id ou None s'il n'existe pas."""
        return cast(list[Message], cls.query.filter(Message.channel_id == channel_id).all())

    @classmethod
    def find_since(cls, channel_id: int, since: int) -> list["Message"]:
        """Retourne les message d'un channel depuis since."""
        return cast(list[Message], cls.query.filter(Message.channel_id == channel_id, Message.id > since).all())
    
    @classmethod
    def find_all(cls) -> list["Message"]:
        """Retourne la liste de tous les tickets."""
        return cast(list[Message], cls.query.all())
    
    @classmethod
    def get_unread_counts_by_channel(cls, user_id: int) -> list:
        """Retourne le nombre de messages non lus par channel pour un user."""
        return (
            db.session.query(cls.channel_id, func.count(cls.id).label('count'))  # pylint: disable=not-callable
            .filter(
                cls.author_id != user_id,
                ~MessageReadStatus.query.filter(
                    MessageReadStatus.message_id == cls.id,
                    MessageReadStatus.user_id == user_id
                ).exists()
            )
            .group_by(cls.channel_id)
            .all()
        )
    
    @classmethod
    def mark_channel_as_read(cls, channel_id: int, user_id: int) -> int:
        """Marque tous les messages non lus d'un channel comme lus pour un user."""
        
        # Récupérer les messages non lus de ce channel pour cet user
        unread_msgs = (
            cls.query
            .filter(
                cls.channel_id == channel_id,
                cls.author_id != user_id,
                ~MessageReadStatus.query.filter(
                    MessageReadStatus.message_id == cls.id,
                    MessageReadStatus.user_id == user_id
                ).exists()
            )
            .all()
        )

        # Insérer un read_status pour chaque message non lu
        for msg in unread_msgs:
            read_status = MessageReadStatus(message_id=msg.id, user_id=user_id)
            db.session.add(read_status)

        db.session.commit()

        return len(unread_msgs)
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at,
            "author_id": self.author_id,
            "channel_id": self.channel_id
        }
    
    @classmethod
    def create(cls, **kwargs) -> "Message":
        ticket = cls(**kwargs)
        db.session.add(ticket)
        db.session.commit()
        return ticket 


class MessageReadStatus(db.Model):
    __tablename__ = 'message_read_status'

    id         = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('Message.id'), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('User.id'),    nullable=False)
    read_at    = db.Column(db.DateTime, default=get_utc_now)

    __table_args__ = (
        db.UniqueConstraint('message_id', 'user_id', name='uq_msg_user'),
    )