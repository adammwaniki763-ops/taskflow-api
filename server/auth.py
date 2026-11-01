from functools import wraps
from flask import Blueprint, jsonify, request, session
from .extensions import bcrypt, db
from .models import User

auth_bp = Blueprint("auth", __name__)

def current_user():
    uid = session.get("user_id")
    return db.session.get(User, uid) if uid else None

def login_required(view):
    @wraps(view)
    def guarded(*args, **kwargs):
        user = current_user()
        if user is None: return jsonify({"error":"Authentication required."}), 401
        return view(user, *args, **kwargs)
    return guarded

def credentials():
    data=request.get_json(silent=True) or {}; name=data.get("username"); password=data.get("password")
    if not isinstance(name,str) or not name.strip(): return None,None,"username is required"
    if not isinstance(password,str) or len(password)<8: return None,None,"password must contain at least 8 characters"
    return name.strip(),password,None

@auth_bp.post("/signup")
def signup():
    name,password,error=credentials()
    if error: return jsonify({"error":error}),400
    if User.query.filter_by(username=name).first(): return jsonify({"error":"username already exists"}),409
    user=User(username=name,password_hash=bcrypt.generate_password_hash(password).decode())
    db.session.add(user); db.session.commit(); session["user_id"]=user.id
    return jsonify(user.to_dict()),201

@auth_bp.post("/login")
def login():
    name,password,error=credentials(); user=User.query.filter_by(username=name).first() if not error else None
    if error or not user or not bcrypt.check_password_hash(user.password_hash,password): return jsonify({"error":"invalid credentials"}),401
    session["user_id"]=user.id; return jsonify(user.to_dict()),200

@auth_bp.get("/check_session")
def check_session():
    user=current_user(); return (jsonify(user.to_dict()),200) if user else (jsonify({"error":"not logged in"}),401)

@auth_bp.post("/logout")
def logout():
    session.clear(); return jsonify({"message":"logged out"}),200
