import sys
from pathlib import Path

import pytest

# Ensure the repository root is on the import path when tests run in CI
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app import create_app, db  # noqa: E402


@pytest.fixture()
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.create_all()
    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
