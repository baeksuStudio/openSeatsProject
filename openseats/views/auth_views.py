
from flask import Blueprint, url_for, render_template, flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from openseats import db
from openseats.forms import UserCreateForm, UserLoginForm
from openseats.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/SignIn')
def SignIn_page() :
    return render_template('sign_in.html')

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
