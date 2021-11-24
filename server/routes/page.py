from flask import Blueprint, jsonify
from sqlalchemy import select
from sqlalchemy.engine import row

from server.db.database import db
from server.db.models import Page, Classification
from server.utils.helpers import token_required, object_as_dict

page_route = Blueprint('page_route', __name__)


@page_route.route('/pages', methods=['GET'])
@token_required
def get_books(current_user):
    pages = Page.query.all()

    output = []
    for page in pages:
        page_result = {'id': page.id, 'name': page.name}
        output.append(page_result)

    return jsonify({'pages': output})


@page_route.route('/page/<int:page_id>', methods=['GET'])
# @token_required
def get_book_classifitications(page_id):

    stmt = select(Page, Classification). \
        join(Classification, Page.id == Classification.page_id). \
        where(Page.id == page_id)
    query = db.session.execute(stmt).all()
    page_classifications = [dict(zip(('page', 'classification'), dat)) for dat in query]

    classifications_payload = []
    for classification in page_classifications:
        classifications_payload.append({
            'page_id': classification['page'].id,
            'classification_id': classification['classification'].id
        })

    payload = {'page_classifications': classifications_payload}

    return payload

    # result = [x.as_dict() for x in page_classifications]
    # pages = Page.query.all()
    #
    # output = []
    # for page in pages:
    #     page_result = {'id': page.id, 'name': page.name}
    #     output.append(page_result)

    # return jsonify({'classifications': ''})

