from app.extensions import db
from datetime import datetime


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # 外键
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    pid = db.Column(db.Integer, db.ForeignKey('posts.id'))
