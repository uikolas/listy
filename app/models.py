from dataclasses import dataclass
from app.extensions import db


# Many-to-many table
user_list = db.Table(
    'user_list',
    db.Column('list_id', db.Integer, db.ForeignKey('list.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    lists = db.relationship('List', secondary=user_list, back_populates='users', lazy=True)

    def add_list(self, list: 'List'):
        self.lists.append(list)


@dataclass
class List(db.Model):
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    list_items = db.relationship('ListItem', backref='list', lazy=True)
    users = db.relationship('User', secondary=user_list, back_populates='lists', lazy=True)

    def has_user(self, current_user: 'User'):
        for user in self.users:
            if user == current_user:
                return True
            return False


@dataclass
class ListItem(db.Model):
    id: int
    name: str
    icon: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)


@dataclass
class Grocery(db.Model):
    id: int
    name: str
    icon: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100), nullable=False)
