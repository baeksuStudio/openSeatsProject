from flask import Blueprint, render_template, abort, request, flash
from werkzeug.utils import redirect

from openseats.models import User
from .auth_views import login_required
from openseats.forms import UserEditForm

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main_page() :
    return render_template('main.html')


@bp.route('/<string:user_page>')
def my_page(user_page) :
    user = User.query.filter_by(userID=user_page).first()
    if user is None :
        abort(404)
    else :
        return render_template('mypage/mypage.html', user=user)

@bp.route('/<string:user_page>/edit', methods=('GET', 'POST'))
@login_required
def my_page_edit(user_page) :
    form = UserEditForm()
    user = User.query.filter_by(userID=user_page).first()
    if request.method == 'POST' and form.validate_on_submit():
        Edituser = User.query.filter_by(username=form.Editusername.data).first()
        Edituser_email = User.query.filter_by(email=form.Editemail.data).first()
        EdituserID = User.query.filter_by(userID=form.EdituserID.data).first()
        if not Edituser :
            if not Edituser_email :
                if not EdituserID :
                    user = User(username=form.Editusername.data,
                            password=generate_password_hash(form.Editpassword1.data),
                            email=form.Editemail.data,
                            userID=form.EdituserID.data,
                            userMessage=form.EdituserMessage.data)
                    db.session.add(user)
                    db.session.commit()
                    
                    return redirect(url_for('main.my_page', user_page=user.userID))
                else :
                    flash('이미 존재하는 사용자 아이디 입니다.')
            else :
                flash('이미 존재하는 사용자 이메일 입니다.')
        else:
            flash('이미 존재하는 사용자 이름 입니다.')

    return render_template('mypage/mypage_edit.html', user=user, form=form)

