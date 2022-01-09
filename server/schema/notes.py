from marshmallow import Schema, fields


class NoteSchema(Schema):
    id = fields.Integer()
    # created_at = fields.DateTime()
    text = fields.String(missing=None)
    classification_id = fields.Integer()


class NoteUpdateSchema(Schema):
    id = fields.Integer()
    # updated_at = fields.DateTime()
    text = fields.String(missing=None)


class NoteAddSchema(Schema):
    # TODO pro required fields musi byt load_default
    # created_at = fields.DateTime(required=True)
    note = fields.String(missing=None)
    classification_id = fields.Integer()
    page_id = fields.Integer()
