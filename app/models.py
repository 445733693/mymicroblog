from app import db
from datetime import datetime


# 在解释器中执行db.create_all()来创建数据库和表

#  定义数据库存储的schema
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # 一对多关系，定义在一的一端，这样可以很方便地根据一获得多
    # 第一个参数'Post'指多端的类名；backref指多端指向一端的字段名，在初始化多端对象时传入会自动初始化多端的外键；
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):  # 这个方法是python里的print出来的方法
        return '<User {}>'.format(self.username)


# 增加数据库的model后，需要执行flask db migrate -m "posts table"
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 外键

    def __repr__(self):
        return '<Post {}>'.format(self.body)
