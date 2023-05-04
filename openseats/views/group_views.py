from flask import Blueprint, render_template, url_for, request
from datetime import datetime
from werkzeug.utils import secure_filename
from openseats import db
# from __main__ import app
from openseats.models import Group
from openseats.forms import GroupForm,ImageForm

import os
bp = Blueprint('group', __name__, url_prefix='/group')

@bp.route('/')
def main_page():
    group_list = Group.query.order_by(Group.create_date.desc())
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
        group = Group(
            name=form.name.data, 
            address=form.address.data, 
            description=form.description.data, 
            money_per_hour=int(form.money_per_hour.data), 
            create_date=datetime.now()
            )
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('group.main_page'))
    return render_template('group/group_create.html', form=form)
   
@bp.route('/img', methods=['GET', 'POST'])
def upload_image():
    form = ImageForm()
    if request.method == 'POST' and form.validate_on_submit():
        file = form.image.data
        filename = secure_filename(file.filename)
      
        # PP_ROOT = os.path.dirname(os.path.abspath(__file__))
        # UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static', 'img')
        # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        # In controller save the file with desired name
        # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(full_filename)


        # original

        file.save('openseats/static/img/' + filename)
        return render_template('group/group_look_img.html', image='img/' + filename)
    return render_template('group/group_img.html', form=form)



