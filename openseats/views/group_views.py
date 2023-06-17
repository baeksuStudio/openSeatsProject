from flask import Blueprint, render_template, url_for, request, current_app, g, abort, flash
from datetime import datetime
from werkzeug.utils import secure_filename, redirect
from openseats import db
# from __main__ import app
from openseats.models import Group, Image, Reservation, User, JoinRequest
from openseats.forms import GroupForm, JoinRequestForm
from .auth_views import login_required  

import os
bp = Blueprint('group', __name__, url_prefix='/group')


@bp.route('/')
def main_page():
    page = request.args.get('page', type=int, default=1)  # 페이지
    group_list = Group.query.order_by(Group.created_at.desc())
    group_list = group_list.paginate(page=page, per_page=12)
    return render_template(
        'group/group.html', 
        group_list=group_list,
        )

@bp.route('/detail/<int:group_id>')
@login_required
def detail_page(group_id): 
    # 이미 가입되어 있는지 확인
    form = JoinRequestForm()
    group = Group.query.get_or_404(group_id)
    status = {
        0: 'not joined',
        1: 'already joined',
        2: 'owner',
        3: 'already request'
    }
    join_status = status[0]

    if g.user == None:
        # 회원정보가 없을 경우
        return abort(404, 'please login')
    else:
        # 회원정보 있을 경우
        user = User.query.get(g.user.id)
        group = Group.query.get(group_id)

        if not user or not group:
            flash("유저와 그룹 정보가 없습니다.", category='danger')
            
        # 유저와 호텔 두개의 정보가 모두 있는 Reservation record가 있는지 확인
        if  Reservation.query.filter_by(user_id=user.id, group_id=group.id).first():
            join_status = status[1]

        if JoinRequest.query.filter_by(user_id=user.id, group_id=group.id).first():
            join_status = status[3]

        # 이 그룹의 주인인 경우 true
        if Group.query.filter_by(user_id=user.id, id=group.id).first():
            join_status = status[2]

    return render_template('group/group_detail.html', group=group, join_status=join_status, form=form)
    
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
            owner=g.user
            )
        db.session.add(group)
        db.session.commit()

        # 이미지 파일 업로드
        if request.files.getlist('images')[0]: #이미지 파일 있을경우, 없을 시 데이터베이스 저장 X
            for n, image_file in enumerate(request.files.getlist('images')):
                file_extension = os.path.splitext(image_file.filename)[1]
                filename = secure_filename(str(n) + file_extension)
                path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(group.id), filename)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                image_file.save(path)

                image = Image(name=filename, path=path, group_id=group.id)
                db.session.add(image)

        db.session.commit()

        flash('성공적으로 그룹이 생성되었습니다.', category='primary')
        return redirect(url_for('group.detail_page', group_id=group.id))
    return render_template('group/group_create.html', form=form)
    

@bp.route('/join_request/<int:group_id>', methods=['POST'])
@login_required
def join_request(group_id):
    form = JoinRequestForm()

    
    user = g.user
    message_title = form.message_title.data
    message_content = form.message_content.data

    join_request = JoinRequest(user_id=user.id, group_id=group_id, message_title=message_title, message_content=message_content)
    db.session.add(join_request)
    db.session.commit()

    flash('성공적으로 가입신청 되었습니다.', category='primary')
    return redirect(url_for('group.detail_page', group_id=group_id))

@bp.route('/accept_join_request/<int:join_request_id>', methods=['POST'])
@login_required  # 로그인된 사용자만 접근 가능하도록 설정
def accept_join_request(join_request_id):
    # 가입 신청 정보 가져오기
    join_request = JoinRequest.query.get(join_request_id)

    owner_id = g.user.id
    request_user_id = join_request.user_id
    group_id = join_request.group.id  # 가입 신청할 그룹 ID
    # 가입 신청이 있는지 확인 및 소유자 확인 로직
    if g.user.id == join_request.group.owner.id:
        # 가입 신청 수락 처리
        reservation = Reservation.query.filter_by(user_id=request_user_id, group_id=group_id)
        # 가입 신청 로직 추가
        reservation = Reservation(user_id=request_user_id, group_id=group_id)
        db.session.add(reservation)

        # 기존 가입 신청 삭제
        db.session.delete(join_request)
        db.session.commit()
        flash(f'새로운 멤버({User.query.get(request_user_id)}) 추가되었습니다.')
        return redirect(url_for('group.detail_page', group_id=group_id))
    else:
        flash('유저나 정보를 찾을 수 없습니다.', category='danger')
        return redirect(url_for('group.detail_page', group_id=group_id))   

    return redirect('/notification')  # 처리 후 알림 확인 페이지로 리다이렉트

@bp.route('/reject_join_request/<int:join_request_id>', methods=['POST'])
@login_required  # 로그인된 사용자만 접근 가능하도록 설정
def reject_join_request(join_request_id):
    # 가입 신청 정보 가져오기
    join_request = JoinRequest.query.get(join_request_id)

    # 가입 신청이 있는지 확인 및 소유자 확인 로직

    # 가입 신청 거절 처리
    # ...

    return redirect('/notification')  # 처리 후 알림 확인 페이지로 리다이렉트
        

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
            flash('유저나 그룹의 정보를 찾을 수 없습니다.', category='danger')
            return redirect(url_for('group.detail_page', group_id=group_id))   

        # 유저와 호텔 두개의 정보가 모두 있는 Reservation record가 있는지 확인
        if Reservation.query.filter_by(user_id=user.id, group_id=group.id).first():
            flash('이미 가입되어 있습니다.', category='danger')
            return redirect(url_for('group.detail_page', group_id=group_id))   
        # 이 그룹의 주인인 경우 
        elif Group.query.filter_by(user_id=user.id, id=group.id).first():
            flash('이 그룹의 소유자 입니다.', category='danger')
            return redirect(url_for('group.detail_page', group_id=group_id))   
        else:
            reservation = Reservation(user_id=user.id, group_id=group_id)
            db.session.add(reservation)
            db.session.commit()
            flash('성공적으로 가입되었습니다.', category='primary')
            return redirect(url_for('group.detail_page', group_id=group_id))
    return redirect(url_for('main.main_page'))

   
    


# (테스트용) 여러개의 group을 만들때 사용하는 테스트 함수
# @bp.route('/create/', methods=('GET', 'POST'))
# @login_required
# def create():
#     form = GroupForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         # 새로운 Group 모델 객체 생성
#         for i in range(300):
#             group = Group(
#                 name=f"test {str(i)}", 
#                 address=form.address.data, 
#                 description=form.description.data, 
#                 money_per_hour=int(form.money_per_hour.data), 
#                 owner=g.user
#                 )
#             db.session.add(group)
#             db.session.commit()

#             # 이미지 파일 업로드
#             # for image_file in request.files.getlist('images'):
#             for n, image_file in enumerate(request.files.getlist('images')):
#                 file_extension = os.path.splitext(image_file.filename)[1]
#                 filename = secure_filename(str(n) + file_extension)
#                 path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(group.id), filename)
#                 os.makedirs(os.path.dirname(path), exist_ok=True)
#                 image_file.save(path)

                
#                 image = Image(name=filename, path=path, group_id=group.id)
#                 db.session.add(image)

#         db.session.commit()

#         return redirect(url_for('group.main_page'))
#     return render_template('group/group_create.html', form=form)