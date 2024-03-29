from marshmallow import Schema, fields

from server.schema.notes import NoteSchema


class CoordinatesSchema(Schema):
    x = fields.Float(required=True)
    y = fields.Float(required=True)


class MarkingSchema(Schema):
    classification_id = fields.Integer(required=True)
    page_id = fields.Integer(required=True)
    x = fields.Float(required=True)
    y = fields.Float(required=True)
    width = fields.Float(required=True)
    height = fields.Float(required=True)
    description = fields.String(missing=None)


class DescriptionSchema(Schema):
    description = fields.String(missing=None)


class ClassificationDetailSchema(Schema):
    page_id = fields.Integer(required=True)
    description = fields.Nested(DescriptionSchema)
    markings = fields.Nested(MarkingSchema(many=True))


class PageClassificationSchema(Schema):
    classification_id = fields.Integer()
    note = fields.Nested(NoteSchema)
    description = fields.String()
    markings = fields.Nested(MarkingSchema(many=True))
    visited = fields.Boolean()
    favorite = fields.Integer()
    user_id = fields.Integer()
    user_name = fields.String()
    created_at = fields.String()
    page_id = fields.Integer()
    page_name = fields.String()


class PageClassificationsSchema(Schema):
    items: fields.Nested(PageClassificationSchema(many=True))
    total_items: fields.Integer()


class PageSchema(Schema):
    id = fields.Integer()
    name = fields.String(missing=None)


class FavoriteSchema(Schema):
    id = fields.Integer()
    classification_id = fields.Integer(required=True)
    page_id = fields.Integer(required=True)
