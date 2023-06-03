from flask import Blueprint, render_template, url_for, request, current_app, g, abort, flash
from datetime import datetime
from werkzeug.utils import secure_filename, redirect
from openseats import db
# from __main__ import app
from openseats.models import Group, Image, Reservation, User
from openseats.forms import GroupForm
from .auth_views import login_required

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
@login_required
def detail_page(group_id): 
    # 이미 가입되어 있는지 확인
    is_joined = False

    if g.user == None:
        # 회원정보가 없을 경우
        return abort(404, 'please login')
    else:
        # 회원정보 있을 경우
        user = User.query.get(g.user.id)
        group = Group.query.get(group_id)
        if not user or not group:
            abort(404, '유져와 그룹 정보가 없습니다.')
        if user.reservation and group.reservation:
            is_joined = True
        else:
            is_joined = False
            
    group = Group.query.get_or_404(group_id)
    return render_template('group/group_detail.html', group=group, is_joined=is_joined)
    

@bp.route('/join/<int:group_id>', methods=['POST'])
def join(group_id):
    # group = Group.query.get_or_404(group_id)
        # user = g.user
    if g.user == None:
        # 회원정보가 없을 경우
        return redirect(url_for(auth.SignIn)) 
    else:
        # 회원정보 있을 경우
        user = User.query.get(g.user.id)
        group = Group.query.get(group_id)
        if not user or not group:
            abort(404, '유져와 그룹 정보가 없습니다.')
        if user.reservation and group.reservation:
            return redirect(url_for('group.detail_page', group_id=group_id))   
        else:
            reservation = Reservation(user_id=g.user.id, group_id=group_id)
            db.session.add(reservation)
            db.session.commit()
            return redirect(url_for('group.detail_page', group_id=group_id))
    return redirect(url_for('main.main_page'))

   
    

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = GroupForm()
    if request.method == 'POST' and form.validate_on_submit():
        # 새로운 Group 모델 객체 생성
        group = Group(
            name=form.name.data, 
            address=form.address.data, 
            description=form.description.data, 
            money_per_hour=int(form.money_per_hour.data), 
            owner=g.user
            )
        db.session.add(group)
        db.session.commit()

        # 이미지 파일 업로드
        for image_file in request.files.getlist('images'):
            filename = secure_filename(image_file.filename)
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(group.id), filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            image_file.save(path)

            
            image = Image(name=filename, path=path, group_id=group.id)
            db.session.add(image)

        db.session.commit()

        return redirect(url_for('group.main_page'))
    return render_template('group/group_create.html', form=form)
