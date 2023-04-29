from flask import Blueprint, render_template, url_for, request
from werkzeug.utils import redirect
from datetime import datetime

from openseats import db
from openseats.models import Group
from openseats.forms import GroupForm

bp = Blueprint('group', __name__, url_prefix='/group')

@bp.route('/')
def main_page():
    group_list = Group.query.order_by(Group.create_date.desc())
    return render_template('group/group.html', group_list=group_list)

@bp.route('/detail/<int:group_id>')
def detail_page(group_id): 
    group = Group.query.get(group_id)
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
    # name = request.form['inputName']
    # address = request.form['inputAddress']
    # description = request.form['inputDescription']
    # money_per_hour = int(request.form['inputPrice'])

    # group = Group(name=name, address=address, description=description, money_per_hour=money_per_hour, create_date=datetime.now())
    # db.session.add(group)
    # db.session.commit()
    # return redirect(url_for('group.main_page'))


