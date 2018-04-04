from app.extensions import db
from flask import current_app, flash
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_login import UserMixin


class User(UserMixin, db.Model):
    # 表名
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String(64),default='default.jpg')

    # 添加关系
    posts =db.relationship('Posts',backref='user',lazy='dynamic')
    comments = db.relationship('Comments', backref='user', lazy='dynamic')
    def __repr__(self):
        return self.username

    # 密码不能直接访问 如果直接访问测报错
    @property
    def password(self):
        raise ArithmeticError('密码不能访问')

    # 设置密码 user.password='1234' 转化成 user.password_hash=hash('1234)
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 生成token
    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        return s.dumps({'id': self.id})

    # 检查密码是否正确
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 检查token是否正确
    @staticmethod
    def check_activate_token(token):
        # 生成Serializer对象
        s = Serializer(current_app.config['SECRET_KEY'])
        # 对解析token进行异常处理
        try:
            data = s.loads(token)
        except BadSignature:
            flash('无效token')
            return False
        except SignatureExpired:
            flash('token已过期')
            return False
        id = data.get('id')
        user = User.query.get(id)
        # 判断用户是否激活
        if not user:
            flash('用户不存在,请重新注册')
            return False
        if not user.confirmed:
            # 设置激活
            user.confirmed = True
            db.session.add(user)
        return True


from app.extensions import login_manager


# 设置flask_login的回调函数 即flask_login获取user对象的方法
@login_manager.user_loader
def load_user(uid):
    user = User.query.get(int(uid))
    return user
