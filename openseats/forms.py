from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename


class GroupForm(FlaskForm):
    name = StringField('제목', validators=[DataRequired('제목은 필수 항목입니다.')])
    address = StringField('주소', validators=[DataRequired('주소는 필수 항목입니다.')])
    description = StringField('설명', validators=[DataRequired('설명은 필수 항목입니다.')])
    money_per_hour = StringField('시간당 금액', validators=[DataRequired('금액은 필수 항목입니다.')])
    image = FileField('image', validators=[FileRequired('이미지 업로드는 필수 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired('이름은 2~15자리로 지어주세요.'), Length(min=2, max=15)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    
class UserLoginForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])

class ImageForm(FlaskForm) :
    image = FileField('image', validators=[FileRequired()])