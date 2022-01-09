import json
from datetime import datetime
from flask import Blueprint, request, Response
from flask_accepts import responds
from sqlalchemy import desc, func
from werkzeug.exceptions import Unauthorized
from server.db.database import db
from server.db.models import Page, Classification, Description, Visited, Note, Marking, Favorite
from server.schema.page import ClassificationDetailSchema, PageClassificationSchema, PageSchema
from server.utils.helpers import token_required, as_dict

page_route = Blueprint('page_route', __name__)

# TODO doplnit bad requesty, co kdyz se nenajde konkretni zaznam, vratit not exists


@page_route.route('/pages', methods=['GET'])
@token_required
@responds(schema=PageSchema(many=True), status_code=200)
def get_pages(current_user):
    pages = Page.query.all()

    output = []
    for page in pages:
        page_result = {'id': page.id, 'name': page.name}
        output.append(page_result)

    return output


@page_route.route('/page/<int:page_id>', methods=['GET'])
# @token_required
@responds(schema=PageClassificationSchema(many=True), status_code=200)
def get_page_classifications(page_id):
    date_to = request.args.get('date_to', datetime.utcnow(), type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    qq = db.session.query(Page, Classification, Visited, Note, Favorite).join(Classification, Page.id == Classification.page_id, isouter=True) \
        .filter(Page.id == page_id).filter(func.date(Classification.created_at) <= func.date(date_to)) \
        .join(Note, Note.classification_id == Classification.id and Note.user_id == 1, isouter=True) \
        .join(Favorite, Favorite.classification_id == Classification.id and Favorite.user_id == 1, isouter=True) \
        .join(Visited, Visited.classification_id == Classification.id and Visited.user_id == 1, isouter=True) \
        .order_by(desc(Classification.created_at)).paginate(page, per_page, error_out=False).items

    page_classifications = [dict(r) for r in qq]

    classifications_payload = []
    for classification in page_classifications:
        if classification['Classification'] is None:
            continue

        classifications_payload.append({
            'classification_id': classification['Classification'].id,
            'note': classification['Note'].text if classification['Note'] else '',
            'description': classification['Classification'].description,
            'markings': json.loads(classification['Classification'].markings),
            'visited': True if classification['Visited'] else False,
            'favorite': True if classification['Favorite'] else False,
            'user_id': classification['Classification'].user_id,
            'user_name': classification['Classification'].user_name,
            'created_at': classification['Classification'].created_at,
        })

    return classifications_payload


@page_route.route('/visit/<int:user_id>', methods=['POST'])
@token_required
def visit(current_user, user_id):
    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    req = request.get_json()
    classification_id = req["classification_id"]

    new_visited_classification = Visited(
        user_id=current_user.id,
        classification_id=classification_id
    )

    db.session.add(new_visited_classification)
    db.session.commit()

    status_code = Response(status=201)
    return status_code


@page_route.route('/favorite/<int:user_id>', methods=['POST'])
@token_required
def add_to_favorites(current_user, user_id):
    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    req = request.get_json()
    classification_id = req["classification_id"]

    new_favorite = Favorite(
        user_id=current_user.id,
        classification_id=classification_id
    )

    db.session.add(new_favorite)
    db.session.commit()

    status_code = Response(status=201)
    return status_code


@page_route.route('/favorite/<int:user_id>', methods=['DELETE'])
@token_required
def delete_from_favorites(current_user, user_id):
    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    req = request.get_json()
    favorite_id = req["favorite_id"]

    Favorite.query.filter(Favorite.id == favorite_id).delete()
    db.session.commit()

    status_code = Response(status=204)
    return status_code


# TODO NOT WORKING
@page_route.route('/classification/<int:classification_id>', methods=['GET'])
# @token_required
@responds(ClassificationDetailSchema, status_code=200)
def classification_details(classification_id):

    markings = Marking.query.filter_by(classification_id=classification_id).all()
    description = Description.query.filter_by(classification_id=classification_id).first()

    # TODO page_id?? bude vubec tento endpoint k necemu?

    classifications_payload = {
        # 'page_id': description.page_id,
        'description': description if description else None,
        'markings': [as_dict(x) for x in markings]
    }

    return classifications_payload


@page_route.route('/classification/user', methods=['GET'])
# @token_required
@responds(schema=PageClassificationSchema(many=True), status_code=200)
def users_classifiations():
    user_name = request.args.get('user_name')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    qq = db.session.query(Classification, Visited, Note, Favorite).filter_by(user_name=user_name) \
        .join(Note, Note.classification_id == Classification.id and Note.user_id == 1, isouter=True) \
        .join(Favorite, Favorite.classification_id == Classification.id and Favorite.user_id == 1, isouter=True) \
        .join(Visited, Visited.classification_id == Classification.id and Visited.user_id == 1, isouter=True) \
        .order_by(desc(Classification.created_at)).paginate(page, per_page, error_out=False).items

    page_classifications = [dict(r) for r in qq]

    classifications_payload = []
    for classification in page_classifications:
        if classification['Classification'] is None:
            continue

        classifications_payload.append({
            'classification_id': classification['Classification'].id,
            'note': classification['Note'].text if classification['Note'] else '',
            'description': classification['Classification'].description if classification[
                'Classification'].description else '',
            'markings': json.loads(classification['Classification'].markings),
            'visited': True if classification['Visited'] else False,
            'favorite': True if classification['Favorite'] else False,
            'user_id': classification['Classification'].user_id,
            'user_name': classification['Classification'].user_name,
            'created_at': classification['Classification'].created_at,
        })

    payload = {'page_classifications': classifications_payload}

    return classifications_payload


@page_route.route('/classification/note/<int:user_id>', methods=['GET'])
# @token_required
@responds(schema=PageClassificationSchema(many=True), status_code=200)
def get_all_with_note(user_id):
    # if not (current_user.id == user_id):
    #     raise Unauthorized('Unauthorized.')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    qq = db.session.query(Classification, Note, Favorite).join(Note, Note.classification_id == Classification.id and Note.user_id == 1)\
        .join(Favorite, Favorite.classification_id == Classification.id and Favorite.user_id == 1, isouter=True) \
        .order_by(desc(Classification.created_at)).paginate(page, per_page, error_out=False).items

    page_classifications = [dict(r) for r in qq]

    classifications_payload = []
    for classification in page_classifications:
        if classification['Classification'] is None:
            continue

        classifications_payload.append({
            'classification_id': classification['Classification'].id,
            'note': classification['Note'].text if classification['Note'] else '',
            'description': classification['Classification'].description if classification['Classification'].description else '',
            'markings': json.loads(classification['Classification'].markings),
            'visited': True,
            'favorite': True if classification['Favorite'] else False,
            'user_id': classification['Classification'].user_id,
            'user_name': classification['Classification'].user_name,
            'created_at': classification['Classification'].created_at,
        })

    payload = {'page_classifications': classifications_payload}

    return classifications_payload
