"""Minimal Flask application setup for the SQLAlchemy assignment."""
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

# These extension instances are shared across the app and models
# so that SQLAlchemy can bind to the application context when the
# factory runs.
from werkzeug.exceptions import BadRequest, NotFound, Conflict

from models import db  
migrate = Migrate()


def create_app(test_config=None):
    """Application factory used by Flask and the tests."""

    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

  # Import models here so SQLAlchemy is aware of them before migrations
    # or ``create_all`` run. Students will flesh these out in ``models.py``.
    from models import User, Post

  

    @app.route("/")
    def index():
        """Simple sanity check route."""
        return jsonify({"message": "Welcome to the Flask + SQLAlchemy assignment"})

    @app.route("/users", methods=["GET", "POST"])
    def users():
        """List or create users."""
        if request.method == "GET":
            users = User.query.order_by(User.id).all()
            return jsonify([{"id": u.id, "username": u.username} for u in users]), 200

        if request.method == "POST":
            if not request.is_json:
                raise BadRequest("Request must be JSON")
            data = request.get_json()
            username = (data.get("username") or "").strip()
            if not username:
                raise BadRequest("Missing 'username' field")
            if User.query.filter_by(username=username).first():
                raise Conflict("Username already exists")
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
            return jsonify({"id": user.id, "username": user.username}), 201

    @app.route("/posts", methods=["GET", "POST"])
    def posts():
        """List or create posts."""
        if request.method == "GET":
            posts = Post.query.order_by(Post.id).all()
            result = []
            for p in posts:
                author = p.author
                result.append({
                    "id": p.id,
                    "title": p.title,
                    "content": p.content,
                    "user_id": p.user_id,
                    "author": {"id": author.id, "username": author.username} if author else None
                })
            return jsonify(result), 200

        if request.method == "POST":
            if not request.is_json:
                raise BadRequest("Request must be JSON")
            data = request.get_json()
            title = (data.get("title") or "").strip()
            content = data.get("content")
            user_id = data.get("user_id")
            if not title:
                raise BadRequest("Missing 'title' field")
            if user_id is None:
                raise BadRequest("Missing 'user_id' field")
            user = User.query.get(user_id)
            if not user:
                raise NotFound(f"User with id={user_id} not found")
            post = Post(title=title, content=content, user_id=user_id)
            db.session.add(post)
            db.session.commit()
            return jsonify({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "user_id": post.user_id,
                "author": {"id": user.id, "username": user.username}
            }), 201

    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return jsonify({"error": str(e)}), 400

    @app.errorhandler(NotFound)
    def handle_not_found(e):
        return jsonify({"error": str(e)}), 404

    @app.errorhandler(Conflict)
    def handle_conflict(e):
        return jsonify({"error": str(e)}), 409

    @app.errorhandler(Exception)
    def handle_exception(e):
        code = getattr(e, "code", 500)
        return jsonify({"error": str(e)}), code

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)