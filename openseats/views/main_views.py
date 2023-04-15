from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main_page() :
    return render_template('main.html')


    
@bp.route('/SignIn')
def SignIn_page() :
    return render_template('sign_in.html')

@bp.route('/SignUp')
def SignUp_page() :
    return render_template('sign_up.html')
