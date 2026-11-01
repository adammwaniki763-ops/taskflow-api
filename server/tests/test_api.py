import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1].parent))
from server.app import create_app
from server.extensions import db

def client():
    app=create_app(testing=True); ctx=app.app_context(); ctx.push(); db.create_all()
    return app.test_client(), ctx

def signup(c, name="alice"):
    return c.post("/signup", json={"username":name,"password":"password123"})

def test_signup_login_session_logout():
    c,ctx=client(); r=signup(c); assert r.status_code==201
    assert c.get("/check_session").status_code==200
    assert c.post("/logout").status_code==200
    assert c.get("/check_session").status_code==401
    assert c.post("/login", json={"username":"alice","password":"password123"}).status_code==200
    ctx.pop()

def test_duplicate_and_bad_login():
    c,ctx=client(); signup(c); assert signup(c).status_code==409
    assert c.post("/login", json={"username":"alice","password":"wrongpass"}).status_code==401
    ctx.pop()

def test_protected_task_crud_and_pagination():
    c,ctx=client(); assert c.get("/tasks").status_code==401; signup(c)
    r=c.post("/tasks", json={"title":"Study","priority":"high"}); assert r.status_code==201
    tid=r.get_json()["id"]; assert c.get("/tasks?page=1&per_page=1").get_json()["total"]==1
    assert c.get(f"/tasks/{tid}").status_code==200
    assert c.patch(f"/tasks/{tid}", json={"completed":True}).status_code==200
    assert c.delete(f"/tasks/{tid}").status_code==200; ctx.pop()

def test_validation_and_ownership():
    c,ctx=client(); signup(c); assert c.post("/tasks", json={"title":""}).status_code==400
    assert c.post("/tasks", json={"title":"X","priority":"urgent"}).status_code==400
    c.post("/tasks", json={"title":"Private"}); c.post("/logout"); signup(c,"brian")
    assert c.get("/tasks/1").status_code==404; ctx.pop()
