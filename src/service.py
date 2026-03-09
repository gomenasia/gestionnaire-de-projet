from src.models import Notification
from app import socketio

def send_notification(user_id, message, notification_type, ticket_id=None):
    Notification.create(
        user_id=user_id,
        message=message,
        type=notification_type,
        ticket_id=ticket_id
    )
    socketio.emit(
        "new_notification",
        {"message": message, "notification_type": notification_type, "ticket_id": ticket_id},
        room=f"user_{user_id}",
    )