from flask import Blueprint
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from flask import request
from flask import jsonify
from flask_login import login_required

from modules.contenttype.models import ContentType
from modules.contenttype.models import ContentItem
from shopyo.api.html import notify_success

contenttype_blueprint = Blueprint(
    "contenttype",
    __name__,
    url_prefix="/contenttype",
    template_folder="templates",
)


@contenttype_blueprint.route("/")
def index():
    return redirect(url_for("contenttype.dashboard"))


@contenttype_blueprint.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    context = {}
    content_types = ContentType.query.all()
    context.update({
        "content_types": content_types
    })
    return render_template('contenttype/dashboard.html', **context)


@contenttype_blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        
        # We'll receive field names and types as lists
        field_names = request.form.getlist("field_name[]")
        field_types = request.form.getlist("field_type[]")
        
        schema = []
        for n, t in zip(field_names, field_types):
            if n:
                schema.append({"name": n, "type": t})
        
        if not name or not schema:
            flash("Name and at least one field are required", "danger")
            return redirect(url_for("contenttype.create"))
            
        new_type = ContentType(name=name, description=description, schema=schema)
        new_type.insert()
        
        flash(f"Content Type '{name}' created!", "success")
        return redirect(url_for("contenttype.dashboard"))

    return render_template('contenttype/create.html')


@contenttype_blueprint.route("/type/<int:type_id>/delete", methods=["GET"])
@login_required
def delete_type(type_id):
    content_type = ContentType.query.get_or_404(type_id)
    content_type.delete()
    flash("Content Type deleted", "success")
    return redirect(url_for("contenttype.dashboard"))


@contenttype_blueprint.route("/type/<int:type_id>/items")
@login_required
def items(type_id):
    content_type = ContentType.query.get_or_404(type_id)
    items = ContentItem.query.filter_by(content_type_id=type_id).all()
    context = {
        "content_type": content_type,
        "items": items
    }
    return render_template('contenttype/items.html', **context)


@contenttype_blueprint.route("/type/<int:type_id>/item/add", methods=["GET", "POST"])
@login_required
def item_add(type_id):
    content_type = ContentType.query.get_or_404(type_id)
    
    if request.method == "POST":
        data = {}
        for field in content_type.schema:
            data[field['name']] = request.form.get(field['name'])
            
        new_item = ContentItem(content_type_id=type_id, data=data)
        new_item.insert()
        flash("Item added", "success")
        return redirect(url_for("contenttype.items", type_id=type_id))
        
    context = {
        "content_type": content_type
    }
    return render_template('contenttype/item_edit.html', **context)


@contenttype_blueprint.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def item_edit(item_id):
    item = ContentItem.query.get_or_404(item_id)
    content_type = item.content_type
    
    if request.method == "POST":
        data = {}
        for field in content_type.schema:
            data[field['name']] = request.form.get(field['name'])
            
        item.data = data
        item.update()
        flash("Item updated", "success")
        return redirect(url_for("contenttype.items", type_id=content_type.id))
        
    context = {
        "content_type": content_type,
        "item": item
    }
    return render_template('contenttype/item_edit.html', **context)


@contenttype_blueprint.route("/item/<int:item_id>/delete")
@login_required
def item_delete(item_id):
    item = ContentItem.query.get_or_404(item_id)
    type_id = item.content_type_id
    item.delete()
    flash("Item deleted", "success")
    return redirect(url_for("contenttype.items", type_id=type_id))
