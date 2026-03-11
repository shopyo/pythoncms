from flask import Blueprint
from flask import jsonify
from flask import request
from modules.contenttype.models import ContentType
from modules.contenttype.models import ContentItem

api_blueprint = Blueprint(
    "api",
    __name__,
    url_prefix="/api/v1",
)

@api_blueprint.route("/<string:type_name>", methods=["GET"])
def get_content(type_name):
    content_type = ContentType.query.filter_by(name=type_name).first()
    if not content_type:
        return jsonify({"error": "Content type not found"}), 404
    
    items = ContentItem.query.filter_by(content_type_id=content_type.id).all()
    
    data = []
    for item in items:
        item_data = {
            "id": item.id,
            "created_at": item.created_at.isoformat(),
            "updated_at": item.updated_at.isoformat(),
            "content": item.data
        }
        data.append(item_data)
        
    return jsonify({
        "count": len(data),
        "data": data
    })

@api_blueprint.route("/types", methods=["GET"])
def get_types():
    content_types = ContentType.query.all()
    data = []
    for ct in content_types:
        data.append({
            "id": ct.id,
            "name": ct.name,
            "description": ct.description,
            "schema": ct.schema
        })
    return jsonify(data)
