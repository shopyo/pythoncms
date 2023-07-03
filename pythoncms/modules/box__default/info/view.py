from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required
from init import db
from shopyo.api.forms import flash_errors
from shopyo.api.module import ModuleHelp

mhelp = ModuleHelp(__file__, __name__)
globals()[mhelp.blueprint_str] = mhelp.blueprint
module_blueprint = globals()[mhelp.blueprint_str]


# @module_blueprint.route(mhelp.info["dashboard"] + "/all")
# def index_all():
#     context = {}
#     pages = Page.query.all()

#     context.update({"pages": pages})
#     return render_template("page/all_pages.html", **context)

from modules.box__default.settings.helpers import set_setting
from modules.box__default.settings.helpers import get_setting

@module_blueprint.route(mhelp.info["dashboard"], methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        print(request.form)
        set_setting('SITE_TITLE', request.form['site_title'])
        set_setting('SITE_DESCRIPTION', request.form['site_description'])
    return mhelp.render('dashboard.html', get_setting=get_setting)