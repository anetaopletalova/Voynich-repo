from flask import Blueprint, jsonify
from server.db.models import Page
from server.utils.helpers import token_required

page_route = Blueprint('page_route', __name__)


@page_route.route('/pages', methods=['POST', 'GET'])
@token_required
def get_authors():
    pages = Page.query.all()

    output = []
    for page in pages:
        page_result = {'id': page.id, 'name': page.name}
        output.append(page_result)

    return jsonify({'pages': output})
