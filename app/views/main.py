from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.models import Posts
from app.forms import PostForm
from app.extensions import db
from app.models import Posts, Comments
from app.models import Comments
from flask_login import current_user
from flask_login import login_required
from app.forms import CommentsForm

# 生成蓝本
main = Blueprint('main', __name__)


# 第一个视图函数
@main.route('/', methods=['GET', 'POST'])
# @login_required
def index():
    form = PostForm()
    # 数据合法则保存
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('登录才能发言哦')
            return redirect(url_for('users.login'))
        else:
            user = current_user._get_current_object()
            post = Posts(content=form.content.data, user=user)
            db.session.add(post)
            return redirect(url_for('main.index'))
    # posts = Posts.query.filter_by(rid=0)
    # 指定渲染页数 分页代码
    page = request.args.get('page', 1, type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(db.desc(Posts.timestamp)).paginate(page, per_page=6)
    posts = pagination.items
    # 最热 最新 博文
    Topposts = Posts.query.order_by(db.desc(Posts.views))[:5]
    Newposts = Posts.query.order_by(db.desc(Posts.timestamp))[:5]
    return render_template('common/index.html', form=form, posts=posts, Topposts=Topposts, Newposts=Newposts,
                           pagination=pagination)


# 博文详情
@main.route('/detail/<int:postid>/', methods=['GET', 'POST'])
def detail(postid):
    form = CommentsForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('登录才能评论哦')
            return redirect(url_for('users.login'))
        else:
            user = current_user._get_current_object()
            post = Posts.query.get(postid)
            comment = Comments(content=form.content.data, user=user, post=post)
            db.session.add(comment)
            return redirect(url_for('main.detail', postid=postid))
    post = Posts.query.get(postid)
    # 阅读数+1
    post.views += 1
    db.session.add(post)
    # 最热 最新 博文
    Topposts = Posts.query.order_by(db.desc(Posts.views))[:5]
    Newposts = Posts.query.order_by(db.desc(Posts.timestamp))[:5]
    # 博文的评论
    comments = Comments.query.filter_by(post=post).order_by(db.desc(Comments.timestamp))
    return render_template('common/detail.html', post=post, Newposts=Newposts, Topposts=Topposts, form=form,
                           comments=comments)


# 关于我们
@main.route('/about/')
def about():
    Topposts = Posts.query.order_by(db.desc(Posts.views))[:5]
    Newposts = Posts.query.order_by(db.desc(Posts.timestamp))[:5]
    return render_template('common/about.html', Newposts=Newposts, Topposts=Topposts)
