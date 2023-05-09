from flask import Blueprint, render_template, abort
from openseats.models import User
from .auth_views import login_required

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

@bp.route('/<string:user_page>/edit')
@login_required
def my_page_edit(user_page) :
    user = User.query.filter_by(userID=user_page).first()
    return render_template('mypage/mypage_edit.html')

