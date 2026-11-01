from pathlib import Path
from flask import Flask, jsonify
from .auth import auth_bp
from .extensions import bcrypt, db, migrate
from .tasks import tasks_bp

def create_app(testing=False):
    app=Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config.update(SECRET_KEY="change-this-in-production", SQLALCHEMY_TRACK_MODIFICATIONS=False)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskflow.db"
    if testing: app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    db.init_app(app); bcrypt.init_app(app); migrate.init_app(app, db)
    app.register_blueprint(auth_bp); app.register_blueprint(tasks_bp)
    @app.get("/health")
    def health(): return jsonify({"status":"ok", "service":"taskflow"}), 200
    @app.errorhandler(404)
    def not_found(error): return jsonify({"error":"route not found"}), 404
    return app

app=create_app()
if __name__ == "__main__":
    with app.app_context(): db.create_all()
    app.run(port=5555, debug=True)
