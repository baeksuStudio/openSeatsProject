from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, EmailField, MultipleFileField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, StopValidation, Optional
from flask_wtf.file import FileField, FileAllowed, FileRequired 

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from markupsafe import Markup
from collections.abc import Iterable

class MultiFileAllowed(object):
    # 파일 업로드 1개 이상 됐는지, 확장자가 맞는지 확인하는 validator
    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):
        # FileAllowed only expects a single instance of FileStorage
        # if not (isinstance(field.data, FileStorage) and field.data):
        #     return

        # Check that all the items in field.data are FileStorage items
        if not (all(isinstance(item, FileStorage) for item in field.data) and field.data):
            return

        for data in field.data:
            filename = data.filename.lower()

            if isinstance(self.upload_set, Iterable):
                if any(filename.endswith('.' + x) for x in self.upload_set):
                    return

                raise StopValidation(self.message or field.gettext(
                    'File does not have an approved extension: {extensions}'
                ).format(extensions=', '.join(self.upload_set)))

            if not self.upload_set.file_allowed(field.data, filename):
                raise StopValidation(self.message or field.gettext(
                    'File does not have an approved extension.'
                ))

class GroupForm(FlaskForm):
    name = StringField('제목', validators=[DataRequired('제목은 필수 항목입니다.'), Length(max=50)])
    address = StringField('주소', validators=[DataRequired('주소는 필수 항목입니다.')])
    description = StringField('설명', validators=[DataRequired('설명은 필수 항목입니다.')])
    images = MultipleFileField('이미지', validators=[FileAllowed(['jpg', 'png', 'jpeg'], '이미지 파일만 가능합니다.')])

    # 최소한개의 파일을 입력받고, 여러개의 파일을 입력받고 싶을 때
    # images = MultipleFileField('섬네일 이미지', validators=[InputRequired('이미지 업로드는 필수 항목입니다.'), MultiFileAllowed(['jpg', 'png', 'jpeg'], 'jpg, png, jpeg 파일만 업로드 할 수 있습니다.')])

class JoinRequestForm(FlaskForm):
    message_title = StringField('제목', validators=[DataRequired('제목은 필수 항목입니다.'), Length(message="메세지는 최대 100글자 입니다.", max=100)])
    message_content = TextAreaField('메세지', validators=[DataRequired('메세지는 필수 항목입니다.')])
    


                
class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(message='사용자이름은 필수 항목입니다.'), Length(message='이름은 2~15자리로 지어주세요.', min=2, max=15)])
    email = EmailField('이메일', validators=[DataRequired(), Email(message='유효한 이메일 주소를 입력하세요')])
    userID = StringField('유저 아이디', validators=[DataRequired(message='유저 아이디는 필수 항목입니다. '), Length(message='이름은 5~15자리로 지어주세요.', min=5, max=20)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(message='비밀번호를 입력해 주세요'), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired(message='비밀번호를 입력해 주세요')])
    

class UserEditForm(FlaskForm):
    photoUpload = FileField('사진 업로드', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    Nowpassword = PasswordField('현재 비밀번호', validators=[DataRequired(message='비밀번호를 입력해 주세요')])
    
    Editusername = StringField('사용자이름', validators=[DataRequired(message='이름은 2~15자리로 지어주세요.'), Length(message='이름은 2~15자리로 지어주세요.', min=2, max=15)])
    EdituserMessage = StringField('상태 메시지', validators=[Optional(), Length(message='상태 메시지는 0~50글자로 지어주세요.', min=0, max=50)])
    Editemail = EmailField('이메일', validators=[DataRequired(), Email(message='유효한 이메일 주소를 입력하세요')])
    EdituserID = StringField('유저 아이디', validators=[DataRequired(message='이름은 5~20자리로 지어주세요.'), Length(message='이름은 2~15자리로 지어주세요.', min=5, max=20)])
    Editpassword1 = PasswordField('비밀번호', validators=[Optional(), EqualTo('Editpassword2', '비밀번호가 일치하지 않습니다')])
    Editpassword2 = PasswordField('비밀번호확인', validators=[Optional()])

    



class UserLoginForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])


