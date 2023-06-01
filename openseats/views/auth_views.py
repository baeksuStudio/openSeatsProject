
from flask import Blueprint, url_for, render_template, flash, request, session, g, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from openseats import db
from openseats.forms import UserCreateForm, UserLoginForm
from openseats.models import User
import functools
import os

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
            session['login_success'] = True
            
            # 메인페이지 말고 로그인이 필요한곳에서의 요청일 경우
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            # redirect가 따로 필요없는 경우 
            else:
                return redirect(url_for('main.main_page'))
        flash(error)
    return render_template('auth/sign_in.html', form=form)

@bp.route('/SignUp', methods=('GET', 'POST'))
def SignUp_page():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        user_email = User.query.filter(User.email == form.email.data).first()
        userID = User.query.filter(User.userID == form.userID.data).first()
        if user == None :
            if user_email == None :
                if userID == None :
                    user = User(username=form.username.data,
                                password=generate_password_hash(form.password1.data),
                                email=form.email.data,
                                userID=form.userID.data,
                                userMessage='')
                    db.session.add(user)
                    db.session.commit()
                    
                    return redirect(url_for('main.main_page'))
                else:
                    flash('이미 존재하는 사용자 아이디 입니다.')
            else:
                flash('이미 존재하는 사용자 이메일 입니다.')
        else:
            flash('이미 존재하는 사용자 이름 입니다.')
        
    return render_template('auth/sign_up.html', form=form)


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
        user_profile_path = os.path.join(current_app.config['USER_PROFILE'],str(user_id))
        if os.path.exists(user_profile_path) :
            g.user_profile_path = url_for('static', filename = "img/profile/{}/profile.png".format(user_id))
        else :
            g.user_profile_path = url_for('static', filename = "img/profile/default_profile.png")
        g.user = User.query.get(user_id)


#  로그인 되어있는지 확인하는 데코레이터 함수
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.SignIn_page', next=_next))
        return view(*args, **kwargs)
    return wrapped_view