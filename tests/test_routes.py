from app import db
from models import Post, User


def test_create_user_route(client, app):
    response = client.post("/users", json={"username": "newuser"})
    assert response.status_code == 201, "POST /users should create a user"

    data = response.get_json()
    assert data["username"] == "newuser"

    with app.app_context():
        assert User.query.count() == 1


def test_list_users_route(client, app):
    with app.app_context():
        db.session.add(User(username="student"))
        db.session.commit()

    response = client.get("/users")
    assert response.status_code == 200
    payload = response.get_json()
    assert isinstance(payload, list)
    assert payload[0]["username"] == "student"


def test_create_and_list_posts(client, app):
    with app.app_context():
        user = User(username="poster")
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    post_resp = client.post(
        "/posts",
        json={"title": "First", "content": "Body", "user_id": user_id},
    )
    assert post_resp.status_code == 201, "POST /posts should create a post"

    list_resp = client.get("/posts")
    assert list_resp.status_code == 200
    posts = list_resp.get_json()
    assert posts[0]["title"] == "First"
    assert posts[0]["username"] == "poster"


def test_posts_require_valid_user(client):
    post_resp = client.post(
        "/posts", json={"title": "Oops", "content": "No user", "user_id": 999}
    )
    assert post_resp.status_code == 400
