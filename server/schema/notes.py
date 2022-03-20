from marshmallow import Schema, fields


class NoteSchema(Schema):
    id = fields.Integer()
    text = fields.String(missing=None)
    classification_id = fields.Integer(required=True)
    page_id = fields.Integer(required=True)


class NoteUpdateSchema(Schema):
    note_id = fields.Integer(attribute="id", required=True)
    text = fields.String(required=True)


class NoteAddSchema(Schema):
    text = fields.String(required=True)
    classification_id = fields.Integer(required=True)
    page_id = fields.Integer(required=True)
