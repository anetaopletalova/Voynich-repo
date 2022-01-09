from marshmallow import Schema, fields, post_load, validate


class UserSchema(Schema):
    user_id = fields.Integer(attribute="id")
    email = fields.Email(validate=validate.Length(min=0, max=50), required=True)
    password = fields.String(metadata={'description': 'password required'},
                             validate=validate.Length(min=0, max=50),
                             load_only=True, required=True)

    # @post_load
    # def make_object(self, data, **kwargs):
    #     return User(**data)


class UserLoginSchema(Schema):
    user = fields.Integer()
    token = fields.String()
    refresh_token = fields.String()


class UserSignUpSchema(Schema):
    email = fields.Email(validate=validate.Length(min=0, max=50))
    password = fields.String(validate=validate.Length(min=0, max=50), load_only=True)
