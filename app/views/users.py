from flask import Blueprint, render_template, flash, current_app, redirect, url_for, request
from app.forms import RegisterForm, LoginForm, ChangePasswordForm, IconForm
from app.models import User,Posts
from app.extensions import db
from app.email import send_mail
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import photos
from PIL import Image
import os

# 生成蓝本
users = Blueprint('users', __name__)


# 注册视图函数
@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 合法保存用户
        user = User(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data
        )
        db.session.add(user)
        db.session.commit()
        # 生成token
        token = user.generate_activate_token()
        # 发邮件
        # send_mail(form.email.data, '激活邮件', 'email/activate', username=form.username.data, token=token)
        # 提示用户邮件已发送,请去激活
        # flash('邮件已发送,请进入激活邮件点击链接激活')
        flash('注册成功请前往登录')
        return redirect(url_for('main.index'))

    return render_template('users/register.html', form=form)


@users.route('/activate/<token>')
def activate(token):
    if User.check_activate_token(token):
        flash('激活成功!')
        return redirect(url_for('main.index'))
    else:
        flash('激活失败,请重新注册')
        return redirect(url_for('users.register'))


# 登录
@users.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 判断数据是否合法
    if form.validate_on_submit():
        # 如果合法则根据用户名查找对象
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash('用户或密码错误')
        # 如果 查到则检验密码是否相等
        elif user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('登录成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('用户或密码错误')
            return redirect(url_for('users.login'))

    return render_template('users/login.html', form=form)


# 注销
@users.route('logout')
def logout():
    logout_user()
    flash('注销成功')
    return redirect(url_for('main.index'))


# 登录才能访问测试
@users.route('/test/')
@login_required
def test():
    return '登录才能测试'


# 个人详情
@users.route('/profile/')
def profile():
    # 取出对象
    user = current_user._get_current_object()
    img_url = photos.url(user.icon)
    return render_template('users/profile.html', img_url=img_url)


# 修改密码
@users.route('/change_password/', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    # 判断密码是否合法
    if form.validate_on_submit():
        # 判断老密码是否正确
        user = current_user._get_current_object()
        if user.verify_password(form.old_password.data):
            # 取出新密码 就行设置保存
            user.password = form.new_password.data
            db.session.add(user)
            flash('修改成功')
            logout_user()
            # 返回登录
            return redirect(url_for('users.login'))
    return render_template('users/change_password.html', form=form)


# 生成随机字符串
def random_str(length=32):
    import random
    import string
    base_str = string.ascii_lowercase + string.digits
    return ''.join(random.choice(base_str) for _ in range(length))


@users.route('/icon/', methods=['GET', 'POST'])
def icon():
    form = IconForm()
    # 取出对象
    user = current_user._get_current_object()
    # 判断数据是否合法
    if form.validate_on_submit():
        # 生成随机文件名
        suffix = os.path.splitext(form.icon.data.filename)[1]
        filename = random_str() + suffix
        # 保存文件
        photos.save(form.icon.data, name=filename)
        # 生成文件名的绝对路径
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        # 生成缩略图
        image = Image.open(pathname)
        # 修改大小
        image.thumbnail((128, 128))
        image.save(pathname)
        # 删除原头像
        if user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], user.icon))
        # 赋值给icon 属性
        user.icon = filename
        db.session.add(user)
        # 提示用户修改成功
        flash('头像修改成功')
    # 返回URL 路径
    img_url = photos.url(user.icon)
    return render_template('users/icon.html', form=form, img_url=img_url)


# 我的帖子
@users.route('/myposts/')
def myposts():
    user = current_user._get_current_object()
    # posts = Posts.query.filter_by(user=user)
    # posts = user.posts.all()
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(user=user).order_by(db.desc(Posts.timestamp)).paginate(page, per_page=6)
    posts = pagination.items
    return render_template('users/myposts.html',posts=posts,pagination=pagination)
