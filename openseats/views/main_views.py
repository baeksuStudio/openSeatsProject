from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main_page() :
    return render_template('main.html')


    
@bp.route('/Login')
def login_page() :
    return render_template('login.html')
