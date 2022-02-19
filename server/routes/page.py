import json
from datetime import datetime
from flask import Blueprint, request, Response, jsonify
from flask_accepts import responds
from sqlalchemy import desc, func
from werkzeug.exceptions import Unauthorized
from server.db.database import db
from server.db.models import Page, Classification, Visited, Note, Favorite, Marking
from server.schema.notes import NoteSchema
from server.schema.page import PageClassificationsSchema, PageSchema, FavoriteSchema, MarkingSchema
from server.utils.helpers import token_required, as_dict, point_in_polygon
from flask_restx import inputs

page_route = Blueprint('page_route', __name__)


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


@page_route.route('/classification/page/<int:user_id>', methods=['GET'])
@token_required
@responds(schema=PageClassificationsSchema, status_code=200)
def get_page_classifications(current_user, user_id):
    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    date_to = request.args.get('date_to', datetime.utcnow(), type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    favorite = request.args.get('favorite', default=False, type=inputs.boolean)
    withNote = request.args.get('with_note', default=False, type=inputs.boolean)
    page_id = request.args.get('page_id', type=int)
    user_name = request.args.get('user_name')

    qq = db.session.query(Page, Classification, Visited, Note, Favorite).join(Classification, Page.id == Classification.page_id, isouter=True) \
        .filter(Page.id == page_id).filter(func.date(Classification.created_at) <= date_to) \
        .join(Note, Note.classification_id == Classification.id and Note.user_id == current_user.id, isouter= not withNote) \
        .join(Favorite, Favorite.classification_id == Classification.id and Favorite.user_id == current_user.id, isouter= not favorite) \
        .join(Visited, Visited.classification_id == Classification.id and Visited.user_id == current_user.id, isouter=True) \


    if user_name:
        qq = qq.filter(Classification.user_name == user_name).all()

    qq = qq.order_by(desc(Classification.created_at)).paginate(page, per_page, error_out=False)
    page_classifications = [dict(r) for r in qq.items]

    total = qq.total


    classifications_payload = []
    for classification in page_classifications:
        if classification['Classification'] is None:
            continue

        classifications_payload.append({
            'classification_id': classification['Classification'].id,
            'note': NoteSchema().dump(classification['Note']) if classification['Note'] else '',
            'description': classification['Classification'].description,
            'markings': json.loads(classification['Classification'].markings),
            'visited': True if classification['Visited'] else False,
            'favorite': classification['Favorite'].id if classification['Favorite'] else None,
            'user_id': classification['Classification'].user_id,
            'user_name': classification['Classification'].user_name,
            'created_at': classification['Classification'].created_at,
            'page_id': classification['Classification'].page_id,
            'page_name': classification['Page'].name,
        })

    return jsonify({'items': classifications_payload, 'total_items': total})


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
@responds(FavoriteSchema, status_code=201)
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
    db.session.flush()

    return jsonify({'favorite_id': new_favorite.id})


@page_route.route('/favorite/<int:user_id>', methods=['DELETE'])
@token_required
def delete_from_favorites(current_user, user_id):
    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    favorite_id = request.args.get('favorite_id')

    Favorite.query.filter(Favorite.id == favorite_id).delete()
    db.session.commit()

    status_code = Response(status=204)
    return status_code

@page_route.route('/classification/all/<int:user_id>', methods=['GET'])
@token_required
@responds(schema=PageClassificationsSchema, status_code=200)
def get_all_classifications(current_user, user_id):
    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    date_to = request.args.get('date_to', datetime.utcnow(), type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    favorite = request.args.get('favorite', default=False, type=inputs.boolean)
    withNote = request.args.get('with_note', default=False, type=inputs.boolean)
    user_name = request.args.get('user_name')
    qq = db.session.query(Page, Classification, Visited, Note, Favorite).join(Classification,
                                                                              Page.id == Classification.page_id,
                                                                              isouter=True) \
        .filter(func.date(Classification.created_at) <= date_to) \
        .join(Note, Note.classification_id == Classification.id and Note.user_id == current_user.id,
              isouter=not withNote) \
        .join(Favorite, Favorite.classification_id == Classification.id and Favorite.user_id == current_user.id,
              isouter=not favorite) \
        .join(Visited, Visited.classification_id == Classification.id and Visited.user_id == current_user.id,
              isouter=True)

    if user_name:
        qq = qq.filter(Classification.user_name == user_name)

    qq = qq.order_by(desc(Classification.created_at)).paginate(page, per_page, error_out=False)

    page_classifications = [dict(r) for r in qq.items]

    total = qq.total


    classifications_payload = []
    for classification in page_classifications:
        if classification['Classification'] is None:
            continue

        classifications_payload.append({
            'classification_id': classification['Classification'].id,
            'note': NoteSchema().dump(classification['Note']) if classification['Note'] else '',
            'description': classification['Classification'].description if classification[
                'Classification'].description else '',
            'markings': json.loads(classification['Classification'].markings),
            'visited': True if classification['Visited'] else False,
            'favorite': classification['Favorite'].id if classification['Favorite'] else None,
            'user_id': classification['Classification'].user_id,
            'user_name': classification['Classification'].user_name,
            'created_at': classification['Classification'].created_at,
            'page_id': classification['Classification'].page_id,
            'page_name': classification['Page'].name,
        })

    return jsonify({'items': classifications_payload, 'total_items': total})


@page_route.route('/markings/<int:page_id>', methods=['GET'])
@token_required
@responds(schema=MarkingSchema(many=True), status_code=200)
def get_markings_by_coordinates(current_user, page_id):
    if not current_user.id:
        raise Unauthorized('Unauthorized.')

    x = request.args.get('x', type=float)
    y = request.args.get('y', type=float)

    query = db.session.query(Marking).filter(Marking.page_id == page_id).all()
    markings = [as_dict(r) for r in query]

    selected_polygons = []
    for marking in markings:
        if point_in_polygon([x, y], marking['x'], marking['y'], marking['width'], marking['height']):
            selected_polygons.append(marking)

    return jsonify({'items': selected_polygons})
