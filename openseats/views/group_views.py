from flask import Blueprint, render_template, url_for, request, current_app
from datetime import datetime
from werkzeug.utils import secure_filename, redirect
from openseats import db
# from __main__ import app
from openseats.models import Group, Image
from openseats.forms import GroupForm

import os
bp = Blueprint('group', __name__, url_prefix='/group')

@bp.route('/')
def main_page():
    group_list = Group.query.order_by(Group.created_at.desc())
    groups = Group.query.all()
    return render_template(
        'group/group.html', 
        group_list=group_list,
        groups=groups
        )

@bp.route('/detail/<int:group_id>')
def detail_page(group_id): 
    group = Group.query.get_or_404(group_id)
    # path = os.path.join('static', 'Image')
    # image = file = os.path.join(path, '.png')
    return render_template('group/group_detail.html', group=group)

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = GroupForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 새로운 Group 모델 객체 생성
        group = Group(
            name=form.name.data, 
            address=form.address.data, 
            description=form.description.data, 
            money_per_hour=int(form.money_per_hour.data), 
            )
        db.session.add(group)
        db.session.commit()

        # 이미지 파일 업로드
        for image_file in request.files.getlist('images'):
            filename = secure_filename(image_file.filename)
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(group.id), filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            image_file.save(path)

            
            image = Image(name=filename, path=filename, group_id=group.id)
            db.session.add(image)

        db.session.commit()

        return redirect(url_for('group.main_page'))
    return render_template('group/group_create.html', form=form)
   
# original
# @bp.route('/create/', methods=('GET', 'POST'))
# def create():
#     form = GroupForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         # image handle
#         file = form.image.data
#         filename = secure_filename(file.filename)
#         group = Group(
#             name=form.name.data, 
#             address=form.address.data, 
#             description=form.description.data, 
#             money_per_hour=int(form.money_per_hour.data), 
#             create_date=datetime.now(),
#             image_path=filename
#             )
#         file.save('openseats/static/img/' + filename)
#         db.session.add(group)
#         db.session.commit()
#         return redirect(url_for('group.main_page'))
#     return render_template('group/group_create.html', form=form)
