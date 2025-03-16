from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from  datetime import datetime

app = Flask(__name__)
db = SQLAlchemy()
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,unique=True)
    username = db.Column(db.String(20), nullable=False)
    password_hash= db.Column(db.String(128), nullable=False)
    role= db.Column(db.String(20), nullable=False,default='user')
    records = db.relationship('Borrowrecord', backref='user', lazy=True)

class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')
    records = db.relationship('Borrowrecord', backref='device', lazy=True)

class Borrowrecord(db.Model):
    __tablename__ = 'borrowrecord'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    borrow_date = db.Column(db.DateTime, default=datetime.now())
    return_date = db.Column(db.DateTime)


if __name__ == '__main__':
    app.run(debug=True)