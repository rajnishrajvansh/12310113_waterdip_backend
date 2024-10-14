from task_management_server.src.models import db
from task_management_server.src.app import app

with app.app_context():
    db.create_all()
