from flask import Blueprint
from common.helpers import render_form_page
from common.login import login_required

admin = Blueprint('admin', __name__,
                  template_folder='templates')

managed = []


@admin.route('/')
@login_required
def admin_home_page():
    global managed
    t = [m() for m in managed]
    return render_form_page("admin/all.html", tables=t)
