from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, EmailField, MultipleFileField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename



class GroupForm(FlaskForm):
    name = StringField('제목', validators=[DataRequired('제목은 필수 항목입니다.'), Length(max=50)])
    address = StringField('주소', validators=[DataRequired('주소는 필수 항목입니다.')])
    description = StringField('설명', validators=[DataRequired('설명은 필수 항목입니다.')])
    money_per_hour = StringField('시간당 금액', validators=[DataRequired('금액은 필수 항목입니다.')])
    # images = MultipleFileField('이미지', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only')])
    images = MultipleFileField('Images', validators=[DataRequired('이미지 업로드는 필수 항목입니다.'), FileAllowed(['jpg', 'png', 'jpeg'], 'Image only')])



class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(message='이름은 2~15자리로 지어주세요.'), Length(message='이름은 2~15자리로 지어주세요.', min=2, max=15)])
    email = EmailField('이메일', validators=[DataRequired(), Email(message='유효한 이메일 주소를 입력하세요')])
    userID = StringField('유저 아이디', validators=[DataRequired(message='이름은 5~20자리로 지어주세요.'), Length(message='이름은 2~15자리로 지어주세요.', min=5, max=20)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(message='비밀번호를 입력해 주세요'), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired(message='비밀번호를 입력해 주세요')])
    

class UserEditForm(FlaskForm):
    Nowpassword = PasswordField('현재 비밀번호', validators=[DataRequired(message='비밀번호를 입력해 주세요')])
    
    Editusername = StringField('사용자이름', validators=[DataRequired(message='이름은 2~15자리로 지어주세요.'), Length(message='이름은 2~15자리로 지어주세요.', min=2, max=15)])
    EdituserMessage = StringField('상태 메시지', validators=[Optional(), Length(message='상태 메시지는 0~50글자로 지어주세요.', min=0, max=50)])
    Editemail = EmailField('이메일', validators=[DataRequired(), Email(message='유효한 이메일 주소를 입력하세요')])
    EdituserID = StringField('유저 아이디', validators=[DataRequired(message='이름은 5~20자리로 지어주세요.'), Length(message='이름은 2~15자리로 지어주세요.', min=5, max=20)])
    Editpassword1 = PasswordField('비밀번호', validators=[Optional(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    Editpassword2 = PasswordField('비밀번호확인', validators=[Optional()])


class UserLoginForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])

