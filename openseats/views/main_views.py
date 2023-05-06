from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main_page() :
    return render_template('main.html')


@bp.route('/<string:user_page>')
def my_page(user_page) :
    return render_template('mypage.html')