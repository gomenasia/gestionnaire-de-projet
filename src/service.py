from src.models import Notification
from app import socketio

def send_notification(receiver_id, message, notification_type, ticket_id=None):
    Notification.create(
        receiver_id=receiver_id,
        message=message,
        type=notification_type,
        ticket_id=ticket_id
    )
    socketio.emit(
        "new_notification",
        {"message": message, "notification_type": notification_type, "ticket_id": ticket_id},
        room=f"user_{receiver_id}",
    )

    socketio.emit( #TODO
        "unread_notif_update",
        "from_user": receiver_id,
    }, room=f'user_{receiver_id}')