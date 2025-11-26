from app import db, app
from models import User, Post

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="alice").first():
        alice = User(username="alice")
        db.session.add(alice)
        db.session.commit()
    else:
        alice = User.query.filter_by(username="alice").first()

    if not Post.query.first():
        post = Post(title="Mon premier post", content="Ceci est un test.", user_id=alice.id)
        db.session.add(post)
        db.session.commit()

    print(User.query.all())
    print(Post.query.all())
