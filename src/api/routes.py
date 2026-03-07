"""API pour l'application."""

from flask import jsonify, request, g, session
from src.models import Ticket, User, Task, Message
from src.utils import login_required, admin_required, handle_db_errors
from . import api_bp


@api_bp.route("/tickets")
@handle_db_errors
def get_ticket():
    """API pour récupérer les tickets filtrés en JSON."""

    tickets = Ticket.find_all()
    return jsonify([ticket.to_dict() for ticket in tickets]), 200


@api_bp.route("/channel/<int:channel_id>/messages")
@handle_db_errors
def get_messages(channel_id):
    since = request.args.get("since", 0)
    messages = Message.query.filter(
        Message.channel_id == channel_id,
        Message.id > since
    ).all()
    return jsonify([m.to_dict() for m in messages]), 200

@api_bp.route("/addTask", methods=["POST"])
@login_required
def addTask():
    """Pour Ajouter une tache"""
    parent_id = request.args.get("parent_id")
    title = request.form.get("title", "")
    content = request.form.get("content", "")

    try:
        task = Task.create_Task(
            title=title,
            content=content,
            user_id=g.user.id,
            parent_id=parent_id)
        return jsonify({
            "id": task.id,
            "title": task.title,
            "content": task.content,
            "status": task.status,
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/task/<int:task_id>/status", methods=["PATCH"])
def UpdateTaskStatus(task_id: int):
    task = Task.find_by_id(task_id)
    if task is None:
        return jsonify({"success": False, "error": "Task non trouvée"}), 404
    data = request.get_json()
    task.update_status(data["status"])
    parent = Task.find_parent_by_parent_id(task.parent_id)
    if parent is not None:
        return jsonify({
            "success": True,
            "parent_id": parent.id
            }), 200
    else:
        return jsonify({
            "success": True
            }), 200



@api_bp.route("/task/<int:task_id>/update", methods=["GET", "POST"])
def update(task_id):
    task = Task.find_by_id(task_id)
    if task is None:
        return jsonify({"success": False, "error": "Task non trouvée"}), 404
    if request.method == "GET":
        return jsonify({
            "success": True,
            "title": task.title,
            "content": task.content
        }), 200
    else:
        title = request.form.get("title", "")
        content = request.form.get("content", "")
        task.update(title=title, content=content)
        return jsonify({
            "success": True}), 200


@api_bp.route("/task/<int:task_id>/delete", methods=["DELETE"])
@admin_required 
def delete(task_id):
    task = Task.find_by_id(task_id)
    if task is None:
        return jsonify({"success": False, "error": "Task non trouvée"}), 404
    if g.user.id == task.author_id or g.user.is_admin_user():
        task.delete_Task()
        return jsonify({
            "success": True}), 200
    else:
        return jsonify({"success": False, 
                        "error": "Vous n'avez pas la permission de suppprimer cette task"}), 404

@api_bp.route('/session')
def get_session():
    return jsonify({
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'role': session.get('role')
    })