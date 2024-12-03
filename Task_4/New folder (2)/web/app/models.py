from datetime import datetime
from app import db
from flask_login import UserMixin
import uuid

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Note(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user = db.relationship('User', backref=db.backref('notes', lazy=True))

class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.String(36), db.ForeignKey('note.id'), nullable=False)
    username = db.Column(db.String(150), nullable=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    note = db.relationship('Note', backref=db.backref('logs', lazy=True))
