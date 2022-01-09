from marshmallow import Schema, fields


class MarkingSchema(Schema):
    classification_id = fields.Integer(missing=None)
    page_id = fields.Integer(missing=None)
    x = fields.Float(missing=None)
    y = fields.Float(missing=None)
    width = fields.Float(missing=None)
    height = fields.Float(missing=None)
    description = fields.String(missing=None)


class DescriptionSchema(Schema):
    description = fields.String(missing=None)


class ClassificationDetailSchema(Schema):
    page_id = fields.Integer(missing=None)
    description = fields.Nested(DescriptionSchema)
    markings = fields.Nested(MarkingSchema(many=True))


class PageClassificationSchema(Schema):
    classification_id = fields.Integer()
    note = fields.String()
    description = fields.String()
    markings = fields.Nested(MarkingSchema(many=True))
    visited = fields.Boolean()
    favorite = fields.Integer()
    user_id = fields.Integer()
    user_name = fields.String()
    created_at = fields.String()


class PageSchema(Schema):
    id = fields.Integer()
    name = fields.String(missing=None)


class FavoriteSchema(Schema):
    id = fields.Integer()
    classification_id = fields.Integer()
    page_id = fields.Integer()
