import json
from types import SimpleNamespace

from flask import Blueprint, jsonify, request, Response
from sqlalchemy import select, desc
from sqlalchemy.engine import row
from werkzeug.exceptions import Unauthorized

from server.db.database import db
from server.db.models import Page, Classification, Description, Visited, Note, Marking
from server.utils.helpers import token_required

page_route = Blueprint('page_route', __name__)


@page_route.route('/pages', methods=['GET'])
@token_required
def get_pages(current_user):
    pages = Page.query.all()

    output = []
    for page in pages:
        page_result = {'id': page.id, 'name': page.name}
        output.append(page_result)

    return jsonify({'pages': output})


@page_route.route('/page/<int:page_id>', methods=['GET'])
# @token_required
def get_page_classifications(page_id):
    # TODO pagination
    # page = request.args.get('page', 1, type=int)
    # per_page = request.args.get('per_page', 20, type=int)
    # bookings_query = TelehealthBookings.query.filter_by(**query_filter). \
    #     order_by(TelehealthBookings.target_date_utc.desc(),
    #              TelehealthBookings.booking_window_id_start_time_utc.desc()).paginate(page, per_page, error_out=False)
    # record_query = Record.query.paginate(page, per_page, False)
    # total = record_query.total
    # record_items = record_query.items


    # TODO optional argument date from to help filtering
    # req = request.get_json()
    # date_from = req["date_from"]
    # year = request.args.get('year', datetime.now().year, type=int)

    qq = db.session.query(Page, Classification, Visited, Note).join(Classification, Page.id == Classification.page_id, isouter=True)\
        .order_by(desc(Classification.created_at)) \
        .join(Note, Note.classification_id == Classification.id and Note.user_id == 1, isouter=True)\
        .join(Visited, Visited.classification_id == Classification.id and Visited.user_id == 1, isouter=True) \
        .filter(Page.id == page_id).all()

    page_classifications = [dict(r) for r in qq]

    classifications_payload = []
    for classification in page_classifications:
        if classification['Classification'] is None:
            continue
        # print(classification)
        # markings = Marking.query.filter_by(classification_id=classification['Classification'].id).all()
        # description = Description.query.filter_by(classification_id=classification['Classification'].id).first()

        classifications_payload.append({
            'classification_id': classification['Classification'].id,
            'note': classification['Note'].text if classification['Note'] else '',
            'description': classification['Classification'].description if classification['Classification'].description else '',
            'markings': json.loads(classification['Classification'].markings),
            'visited': True if classification['Visited'] else False,
            'user_id': classification['Classification'].user_id,
            'user_name': classification['Classification'].user_name,
            'created_at': classification['Classification'].created_at,
        })

    payload = {'page_classifications': classifications_payload}

    return payload


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

# TODO add/remove to/from favorites


@page_route.route('/note/<int:user_id>', methods=['POST'])
@token_required
def add_note(current_user, user_id):

    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    req = request.get_json()
    note = req["note"]
    classification_id = req["classification_id"]

    new_note = Note(
        user_id=current_user.id,
        classification_id=classification_id,
        text=note
    )

    db.session.add(new_note)
    db.session.commit()

    status_code = Response(status=201)
    return status_code

# TODO edit/delete poznamky
# session.query(Tag).filter_by(tag_id=5).update({'count': Tag.count + 1})
# session.query(Clients).filter(Clients.id == client_id_list).update({'status': status})
# session.commit()
# User.query.filter(User.id == 123).delete()
# session.commit()

@page_route.route('/classification/<int:classification_id>', methods=['GET'])
# @token_required
def classification_details(classification_id, ):
    markings = Marking.query.filter_by(classification_id=classification_id).all()
    description = Description.query.filter_by(classification_id=classification_id).first()

    classifications_payload = {
        'description': json.dumps(description),
        'markings': [x.serialized for x in markings]
    }

    payload = {'page_classifications': classifications_payload}
    return payload


@page_route.route('/classification/user', methods=['GET'])
# @token_required
def users_classifiations():
    user_name = request.args.get('user_name')
    classifications = Classification.query.filter_by(user_name=user_name).all()
    page_classifications = []
    #
    for c in classifications:
        page_classifications.append(c.serialized)

    payload = {'page_classifications': page_classifications}
    return payload


@page_route.route('/classification/note/<int:user_id>', methods=['GET'])
# @token_required
def get_all_with_note(user_id):
    # if not (current_user.id == user_id):
    #     raise Unauthorized('Unauthorized.')

    qq = db.session.query(Classification, Note).join(Note, Note.classification_id == Classification.id and Note.user_id == 1).all() \
        .order_by(desc(Classification.created_at))

    page_classifications = [dict(r) for r in qq]

    classifications_payload = []
    for classification in page_classifications:
        if classification['Classification'] is None:
            continue
        # print(classification)
        # markings = Marking.query.filter_by(classification_id=classification['Classification'].id).all()
        # description = Description.query.filter_by(classification_id=classification['Classification'].id).first()

        classifications_payload.append({
            'classification_id': classification['Classification'].id,
            'note': classification['Note'].text if classification['Note'] else '',
            'description': classification['Classification'].description if classification['Classification'].description else '',
            'markings': json.loads(classification['Classification'].markings),
            'visited': True,
            'user_id': classification['Classification'].id.user_id,
            'user_name': classification['Classification'].id.user_name,
            'created_at': classification['Classification'].id.created_at,
        })

    payload = {'page_classifications': classifications_payload}

    return payload
