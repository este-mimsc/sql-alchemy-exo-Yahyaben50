import importlib

from app import create_app, db


def test_create_app_config_overrides():
    app = create_app({"SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    assert app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite://")
    assert app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] is False


def test_models_importable():
    models = importlib.import_module("models")
    assert hasattr(models, "User"), "User model should exist"
    assert hasattr(models, "Post"), "Post model should exist"


def test_db_extension_initialized(app):
    # The extension should be bound to the application context
    assert db.engine.url.database in (":memory:", "blog.db")
