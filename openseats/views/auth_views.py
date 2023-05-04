
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from openseats import db
from openseats.forms import UserCreateForm, UserLoginForm
from openseats.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/SignIn', methods=('GET', 'POST'))
def SignIn_page() :
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            error = "존재하지 않는 이메일입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.main_page'))
        flash(error)
    return render_template('sign_in.html', form=form)

@bp.route('/SignUp', methods=('GET', 'POST'))
def SignUp_page() :
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                    password=generate_password_hash(form.password1.data),
                    email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.main_page'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('sign_up.html', form=form)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.main_page'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)