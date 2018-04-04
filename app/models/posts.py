from app.extensions import db
from datetime import datetime


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, index=True, default=0)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer,default=0)

    # 外键
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship('Comments', backref='post', lazy='dynamic')
