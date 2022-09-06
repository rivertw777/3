from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(32))
    user_pw = db.Column(db.String(32))


class Product(db.Model):
    __tablename__ = 'Product'
    pid = db.Column(db.Integer, primary_key=True)
    uploader = db.Column(db.String(32))
    photo = db.Column(db.String(32))
    name = db.Column(db.String(32))
    price = db.Column(db.String(32))
    check = db.Column(db.String(32))
    keyword = db.Column(db.String(32))
    descript = db.Column(db.String(32))

class FollowData(db.Model):
    __tablename__ = 'Follow'
    fid = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.String(32))
    following = db.Column(db.String(32))

