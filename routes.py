from flask import Blueprint, request, jsonify
from db import get_connection

api_bp = Blueprint('api', __name__)

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)

@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
        task = cursor.fetchone()
    conn.close()
    return jsonify(task or {}), 200

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO tasks (title, completed) VALUES (%s, %s)", 
                       (data['title'], False))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Task created'}), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE tasks SET title=%s, completed=%s WHERE id=%s", 
                       (data['title'], data['completed'], task_id))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Task updated'})

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted'})
