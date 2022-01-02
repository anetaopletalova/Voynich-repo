import jwt
from flask import Blueprint, request, jsonify, make_response, current_app, Response
from werkzeug.exceptions import Unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
from server.db.database import db
from server.db.models import User, Note
from server.utils.helpers import generate_token, token_required

note_route = Blueprint('note_route', __name__)

@note_route.route('/note/<int:user_id>', methods=['POST'])
@token_required
# TODO what is this used for and how
# @responds(schema=StaffCalendarEventsSchema(many=True), status_code=200, api=ns)
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

@note_route.route('/note/<int:user_id>', methods=['PUT'])
# @token_required
def update_note(user_id):

    # if not (current_user.id == user_id):
    #     raise Unauthorized('Unauthorized.')

    req = request.get_json()
    note = req["note"]
    note_id = req["note_id"]

    Note.query.filter_by(id=note_id).update({'text': note})
    db.session.commit()

    payload = {'note': note}
    return payload


@note_route.route('/note/<int:user_id>', methods=['DELETE'])
@token_required
def delete_note(current_user, user_id):

    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    req = request.get_json()
    note_id = req["note_id"]

    Note.query.filter(Note.id == note_id).delete()
    db.session.commit()

    status_code = Response(status=200)
    return status_code
