from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, EmailField, MultipleFileField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, StopValidation
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
    money_per_hour = IntegerField('시간당 금액', validators=[DataRequired()])
    # images = MultipleFileField('이미지', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only')])
    images = MultipleFileField('섬네일 이미지', validators=[InputRequired('이미지 업로드는 필수 항목입니다.'), MultiFileAllowed(['jpg', 'png', 'jpeg'], 'jpg, png, jpeg 파일만 업로드 할 수 있습니다.')])
                
class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired('이름은 2~15자리로 지어주세요.'), Length(min=2, max=15)])
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])
    
class UserLoginForm(FlaskForm):
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[DataRequired()])


