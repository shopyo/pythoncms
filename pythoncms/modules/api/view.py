import os
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

def check_auth():
    token = request.headers.get("Authorization")
    expected_token = os.environ.get("API_TOKEN")
    if expected_token and token != f"Bearer {expected_token}":
        return False
    return True

@api_blueprint.route("/<string:type_name>", methods=["GET"])
def get_content(type_name):
    # Optional Auth
    if os.environ.get("API_TOKEN") and not check_auth():
        return jsonify({"error": "Unauthorized"}), 401

    content_type = ContentType.query.filter_by(name=type_name).first()
    if not content_type:
        return jsonify({"error": "Content type not found"}), 404
    
    # Pagination & Sorting
    limit = request.args.get("limit", default=20, type=int)
    offset = request.args.get("offset", default=0, type=int)
    sort_by = request.args.get("sort_by", default="created_at", type=str)
    order = request.args.get("order", default="desc", type=str)
    
    query = ContentItem.query.filter_by(content_type_id=content_type.id)
    
    # Sorting
    if hasattr(ContentItem, sort_by):
        column = getattr(ContentItem, sort_by)
        if order == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())
            
    total_count = query.count()
    items = query.limit(limit).offset(offset).all()
    
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
        "meta": {
            "count": len(data),
            "total": total_count,
            "limit": limit,
            "offset": offset
        },
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
