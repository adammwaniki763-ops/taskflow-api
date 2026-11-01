from datetime import datetime, timezone
from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    tasks = db.relationship("Task", backref="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "username": self.username,
                "created_at": self.created_at.isoformat()}

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="")
    completed = db.Column(db.Boolean, default=False, nullable=False)
    priority = db.Column(db.String(20), default="medium", nullable=False)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title,
                "description": self.description, "completed": self.completed,
                "priority": self.priority,
                "due_date": self.due_date.isoformat() if self.due_date else None,
                "created_at": self.created_at.isoformat(), "user_id": self.user_id}
