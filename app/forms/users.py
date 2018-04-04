from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.extensions import photos


class RegisterForm(FlaskForm):
    username = StringField('用户名', [Length(4, 12, message='请输入4-12之间的字符')])
    password = PasswordField('密码', [Length(6, 20, message='请输入6-20之间的密码')])
    confirm = PasswordField('密码确认', [EqualTo('password', message='两次密码不一样')])
    email = StringField('邮箱', [Email(message='请输入正确的邮箱')])
    submit = SubmitField('提交')

    # 自定义检验
    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        # 判断user是否存在
        if user:
            # 抛出异常
            raise ValidationError('用户已经存在')

    # 做邮箱检验
    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        # 判断user是否存在
        if user:
            # 抛出异常
            raise ValidationError('邮箱已经存在')


# 登录
class LoginForm(FlaskForm):
    username = StringField('用户名', [DataRequired(message='用户名不能为空')])
    password = PasswordField('密码', [DataRequired(message='密码不能为空')])
    remember = BooleanField('记住我', default=False)
    submit = SubmitField('提交')


# 修改密码
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', [DataRequired(message='原密码不能为空')])
    new_password = PasswordField('新密码', [Length(6, 20, message='请输入6-20之间的密码')])
    confirm = PasswordField('密码确认', [EqualTo('new_password', message='两次密码不一样')])
    submit = SubmitField('提交')

    def validate_new_password(self, field):
        if current_user.verify_password(field.data):
            raise ValidationError('新密码不能和老密码一样')


# 修改头像的form
class IconForm(FlaskForm):
    icon = FileField('头像', [FileRequired(message='请选择上传文件'),
                            FileAllowed(photos, message='请选择图片上传')])
    submit = SubmitField('提交')
