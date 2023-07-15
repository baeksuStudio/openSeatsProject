
from flask import Blueprint, url_for, render_template, flash, request, session, g, current_app
from flask import send_from_directory

import os

bp = Blueprint('feature', __name__, url_prefix='/feature')


@bp.route('/get_profile_image/<int:user_id>')
def get_profile_image(user_id):
    filename = f"{user_id}.png"  
    default_filename = "default_profile.png"  # 기본 프로필 사진 파일 이름

    file_path = os.path.join(current_app.config['USER_PROFILE'], filename)

    if os.path.exists(file_path):
        return send_from_directory(current_app.config['USER_PROFILE'], filename)
    else:
        return send_from_directory(current_app.config['USER_PROFILE'], default_filename)
