from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CommentsForm(FlaskForm):
    content = TextAreaField('', render_kw={'placeholder':'评论要注意分寸哦...','style':'height: 100px;'},validators=[Length(4,400, message='说话要注意分寸')])
    submit = SubmitField('评论')
