from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class GroupForm(FlaskForm):
    name = StringField('제목', validators=[DataRequired('제목은 필수 항목입니다.')])
    address = StringField('주소', validators=[DataRequired('주소는 필수 항목입니다.')])
    description = StringField('설명', validators=[DataRequired('설명은 필수 항목입니다.')])
    money_per_hour = StringField('시간당 금액', validators=[DataRequired('금액은 필수 항목입니다.')])
