from datetime import date, timedelta
from flask_bcrypt import Bcrypt
from .app import create_app
from .extensions import db
from .models import User, Task

app=create_app(); bcrypt=Bcrypt(app)
with app.app_context():
    db.drop_all(); db.create_all()
    alice=User(username="alice",password_hash=bcrypt.generate_password_hash("password123").decode())
    brian=User(username="brian",password_hash=bcrypt.generate_password_hash("password123").decode())
    db.session.add_all([alice,brian]); db.session.flush()
    db.session.add_all([Task(title="Plan weekly goals",description="Review priorities",priority="high",user_id=alice.id),Task(title="Read Flask notes",description="Study auth",priority="medium",user_id=alice.id,due_date=date.today()+timedelta(days=3)),Task(title="Prepare presentation",description="Create slides",priority="low",user_id=brian.id)])
    db.session.commit(); print("Seeded 2 users and 3 tasks.")
