from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    user_id = fields.Integer(attribute="id")
    email = fields.Email(validate=validate.Length(min=0, max=50), required=True)
    password = fields.String(metadata={'description': 'password required'},
                             validate=validate.Length(min=0, max=50),
                             load_only=True, required=True)


class UserLoginSchema(Schema):
    user = fields.Integer(required=True)
    token = fields.String(required=True)
    refresh_token = fields.String(required=True)


class UserSignUpSchema(Schema):
    email = fields.Email(validate=validate.Length(min=0, max=50))
    password = fields.String(validate=validate.Length(min=0, max=50), load_only=True)
