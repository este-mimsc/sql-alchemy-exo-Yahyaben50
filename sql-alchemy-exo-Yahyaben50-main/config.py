"""Basic configuration for the Flask application.

Students can extend or override these defaults as needed for the
assignment. The provided values keep the setup simple for local
development and automated testing.
"""
import os


class Config:
    """Default configuration values for the app."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///blog.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
