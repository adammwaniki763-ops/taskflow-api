from datetime import date
from flask import Blueprint, jsonify, request
from .auth import login_required
from .extensions import db
from .models import Task
tasks_bp=Blueprint("tasks",__name__); VALID_PRIORITIES={"low","medium","high"}
def payload(data,partial=False):
    allowed={"title","description","completed","priority","due_date"}
    if set(data)-allowed: return None,"unknown fields are not allowed"
    if not partial and not isinstance(data.get("title"),str): return None,"title is required"
    if "title" in data and (not isinstance(data["title"],str) or not data["title"].strip()): return None,"title is required"
    if "priority" in data and data["priority"] not in VALID_PRIORITIES: return None,"invalid priority"
    if "completed" in data and not isinstance(data["completed"],bool): return None,"completed must be boolean"
    if data.get("due_date"):
        try: data["due_date"]=date.fromisoformat(data["due_date"])
        except (TypeError,ValueError): return None,"due_date must use YYYY-MM-DD"
    return data,None
@tasks_bp.get("/tasks")
@login_required
def list_tasks(user):
    page=max(request.args.get("page",1,type=int),1); size=min(max(request.args.get("per_page",5,type=int),1),50)
    result=Task.query.filter_by(user_id=user.id).order_by(Task.id).paginate(page=page,per_page=size,error_out=False)
    return jsonify({"tasks":[x.to_dict() for x in result.items],"page":page,"per_page":size,"total":result.total,"pages":result.pages}),200
@tasks_bp.post("/tasks")
@login_required
def create_task(user):
    data,error=payload(request.get_json(silent=True) or {})
    if error: return jsonify({"error":error}),400
    task=Task(user_id=user.id,**data); db.session.add(task); db.session.commit(); return jsonify(task.to_dict()),201
@tasks_bp.get("/tasks/<int:task_id>")
@login_required
def get_task(user,task_id):
    task=Task.query.filter_by(id=task_id,user_id=user.id).first()
    return (jsonify(task.to_dict()),200) if task else (jsonify({"error":"task not found"}),404)
@tasks_bp.patch("/tasks/<int:task_id>")
@login_required
def update_task(user,task_id):
    task=Task.query.filter_by(id=task_id,user_id=user.id).first()
    if not task: return jsonify({"error":"task not found"}),404
    data,error=payload(request.get_json(silent=True) or {},True)
    if error: return jsonify({"error":error}),400
    for key,value in data.items(): setattr(task,key,value)
    db.session.commit(); return jsonify(task.to_dict()),200
@tasks_bp.delete("/tasks/<int:task_id>")
@login_required
def delete_task(user,task_id):
    task=Task.query.filter_by(id=task_id,user_id=user.id).first()
    if not task: return jsonify({"error":"task not found"}),404
    db.session.delete(task); db.session.commit(); return jsonify({"message":"task deleted"}),200
