from flask import Blueprint, request, Response
from flask_accepts import responds, accepts
from werkzeug.exceptions import Unauthorized, BadRequest
from server.db.database import db
from server.db.models import Note
from server.schema.notes import NoteSchema, NoteAddSchema, NoteUpdateSchema
from server.utils.helpers import token_required

note_route = Blueprint('note_route', __name__)


@note_route.route('/note/<int:user_id>', methods=['POST'])
@token_required
@accepts(schema=NoteAddSchema)
@responds(schema=NoteSchema, status_code=201)
def add_note(current_user, user_id):

    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    req = request.get_json()
    note = req["text"]
    classification_id = req["classification_id"]
    page_id = req["page_id"]

    new_note = Note(
        user_id=user_id,
        classification_id=classification_id,
        text=note,
        page_id=page_id
    )

    db.session.add(new_note)
    db.session.commit()
    return new_note


@note_route.route('/note/<int:user_id>', methods=['PUT'])
@token_required
@accepts(NoteUpdateSchema)
@responds(schema=NoteSchema, status_code=201)
def update_note(current_user, user_id):

    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    req = request.get_json()
    note = req["text"]
    note_id = req["note_id"]

    if not note:
        raise BadRequest(f'Content of note missing.')

    res = Note.query.filter_by(id=note_id).update({'text': note})
    db.session.commit()

    result = Note.query.filter(Note.id == note_id).first()
    return result


@note_route.route('/note/<int:user_id>', methods=['DELETE'])
@token_required
def delete_note(current_user, user_id):

    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    note_id = request.args.get("note_id")

    Note.query.filter(Note.id == note_id).delete()
    db.session.commit()
    return Response(status=204)


@note_route.route('/note/<int:user_id>', methods=['GET'])
@token_required
@responds(schema=NoteSchema, status_code=200)
def get_note(current_user, user_id):

    if not (current_user.id == user_id):
        raise Unauthorized('Unauthorized.')

    req = request.get_json()
    note_id = req["note_id"]

    result = Note.query.filter(Note.id == note_id).first()
    return result
