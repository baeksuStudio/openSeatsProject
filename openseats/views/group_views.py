from flask import Blueprint, render_template

from openseats.models import Group

bp = Blueprint('group', __name__, url_prefix='/group')

@bp.route('/')
def main_page() :
    group_list = Group.query.order_by(Group.create_date.desc())
    return render_template('group.html', group_list=group_list)

