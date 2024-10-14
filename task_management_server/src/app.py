from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

@app.route('/v1/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    task = Task(title=data['title'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id}), 201

@app.route('/v1/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()
    return jsonify({'tasks': [{'id': task.id, 'title': task.title, 'is_completed': task.is_completed} for task in tasks]}), 200

@app.route('/v1/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({'error': 'There is no task at that id'}), 404
    return jsonify({'id': task.id, 'title': task.title, 'is_completed': task.is_completed}), 200

@app.route('/v1/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if task is None:
        return jsonify({'error': 'There is no task at that id'}), 404
    data = request.get_json()
    if 'title' in data:
        task.title = data['title']
    if 'is_completed' in data:
        task.is_completed = data['is_completed']
    db.session.commit()
    return jsonify(), 204

@app.route('/v1/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task is not None:
        db.session.delete(task)
        db.session.commit()
    return jsonify(), 204

if __name__ == '__main__':
    app.run(debug=True)
