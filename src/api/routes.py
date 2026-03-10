"""API pour l'application."""

from flask import jsonify, request, session
from src.models import Ticket, Notification, Task, Message
from src.utils import handle_db_errors
from . import api_bp


@api_bp.route("/tickets")
@handle_db_errors
def get_ticket():
    """API pour récupérer les tickets filtrés en JSON."""

    tickets = Ticket.find_all()
    return jsonify([ticket.to_dict() for ticket in tickets]), 200

@api_bp.route("/tasks")
@handle_db_errors
def get_task():
    """API pour récupérer les tache filtrés en JSON."""

    taches = Task.find_all()
    return jsonify([tache.to_dict() for tache in taches]), 200


@api_bp.route("/channel/<int:channel_id>/messages")
@handle_db_errors
def get_messages(channel_id):
    since = request.args.get("since", 0)
    messages = Message.find_since(channel_id, since)
    return jsonify([m.to_dict() for m in messages]), 200

@api_bp.route('/session')
def get_session():
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({
            'success': False,
            'user_id': None,
            'username': None,
            'role': None
        }), 401

    return jsonify({
        'success': True,
        'user_id': user_id,
        'username': session.get('username'),
        'role': session.get('role')
    }), 200

    # ============================= NOTIFICATION =============================

@api_bp.route('/notification/<int:user_id>')
@handle_db_errors
def get_notif_by_user(user_id):
    notifs = Notification.find_by_user(user_id)
    return jsonify([notification.to_dict() for notification in notifs]), 200

@api_bp.route('/notification/unread-counts', methods=['GET']) #RECHECK
def unread_counts():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({}), 401

    counts = (
        db.session.query(Message.sender_id, func.count(Message.id).label('count'))
        .filter(Message.receiver_id == user_id, Message.is_read == False)
        .group_by(Message.sender_id)
        .all()
    )
    return jsonify({str(row.sender_id): row.count for row in counts})


@api_bp.route('/notification/mark-read', methods=['POST'])
def mark_as_read():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Non authentifié'}), 401

    data = request.get_json()
    sender_id = data.get('sender_id')

    updated = (
        Message.query
        .filter_by(sender_id=sender_id, receiver_id=user_id, is_read=False)
        .update({'is_read': True})
    )
    db.session.commit()
    return jsonify({'updated': updated})


    # ===================================== MESSAGE ==============================
