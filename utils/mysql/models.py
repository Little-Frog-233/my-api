import datetime
from utils.mysql.db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   index=True,
                   nullable=False)
    username = db.Column(db.String(255), nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    userpicture = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime,
                            default=datetime.datetime.now,
                            nullable=False)
    update_time = db.Column(db.DateTime,
                            default=datetime.datetime.now,
                            onupdate=datetime.datetime.now,
                            nullable=False)
    user_admin = db.Column(db.Integer, nullable=False, default=0)
    manage = db.Column(db.Integer, nullable=False, default=0)