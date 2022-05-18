import datetime
from blog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False, index=False)
    lastname = db.Column(db.String(50), nullable=False, index=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, index=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now, index=False, unique=False, nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Пользователь {0} {1}>'.format(self.firstname, self.lastname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(1000))
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.title)


