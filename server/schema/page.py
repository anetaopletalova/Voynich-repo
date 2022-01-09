from marshmallow import Schema, fields, post_load, validate
import os
import sys
from app import ma
from server.db.models import User, Classification, Marking, Description

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)



class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_only = 'password'
        dump_only = 'id'

    email = fields.Email(validate=validate.Length(min=0, max=50), required=True)
    password = fields.String(metadata={'description': 'password required'},
                             validate=validate.Length(min=0, max=50),
                             load_only=True, required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return User(**data)


class MarkingSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Marking
        exclude = 'id'
        include_fk = True
    # id = fields.Integer(missing=None)
    # classification_id = fields.Integer(missing=None)
    # page_id = fields.Integer(missing=None)
    # x = fields.Float(missing=None)
    # y = fields.Float(missing=None)
    # width = fields.Float(missing=None)
    # height = fields.Float(missing=None)
    # description = fields.String(missing=None)


class DescriptionSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Description
        exclude = 'id'
        include_fk = True
    # id = fields.Integer(missing=None)
    # page_id = fields.Integer(missing=None)
    # classification_id = fields.Integer(missing=None)
    # description = fields.String(missing=None)


class ClassificationSchema(Schema):
    class Meta:
        model = Classification
        load_only = 'password'
        dump_only = 'id'

    # id = fields.Integer
    # page_id = fields.Integer(missing=None)
    # user_id = fields.Integer(missing=None)
    # user_name = fields.String(missing=None)
    # created_at = fields.String(missing=None)
    # markings = fields.Nested(MarkingSchema(many=True),missing=[])
    # description = fields.Nested(DescriptionSchema,missing=[])
    #
    # @post_load
    # def make_object(self, data, **kwargs):
    #     return Classification(**data)


class PageClassificationSchema(Schema):
    classification_id = fields.Integer
    note = fields.String
    description = fields.Nested(DescriptionSchema)
    markings = fields.Nested(MarkingSchema(many=True))
    visited = fields.Boolean
    favorite = fields.Boolean
    user_id = fields.Integer
    user_name = fields.String
    created_at = fields.DateTime

    @post_load
    def make_object(self, data, **kwargs):
        return Classification(**data)
