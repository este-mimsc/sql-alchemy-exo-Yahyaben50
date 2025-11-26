import pytest

from app import db
from models import Post, User


def test_user_has_required_columns(app):
    columns = User.__table__.columns
    assert "id" in columns, "User.id column is missing"
    assert "username" in columns, "User.username column is missing"

    username_col = columns["username"]
    assert username_col.unique, "username should be unique"
    assert not username_col.nullable, "username should be required"


def test_post_has_required_columns(app):
    columns = Post.__table__.columns
    assert "id" in columns
    assert "title" in columns
    assert "content" in columns
    assert "user_id" in columns

    user_id = columns["user_id"]
    assert user_id.foreign_keys, "user_id should reference users.id"


def test_relationship_between_user_and_post(app):
    user = User(username="author")
    post = Post(title="Hello", content="World", user=user)

    db.session.add_all([user, post])
    db.session.commit()

    assert post.user.username == "author"
    assert user.posts[0].title == "Hello"


@pytest.mark.parametrize(
    "title,content", [("Short", "Body"), ("Another", "More content")]
)
def test_repr_helpers_include_names(title, content, app):
    user = User(username="tester")
    post = Post(title=title, content=content, user=user)
    db.session.add_all([user, post])
    db.session.commit()

    assert "tester" in repr(user)
    assert title in repr(post)
