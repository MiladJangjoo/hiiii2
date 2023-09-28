from marshmallow import Schema, fields

class ReviewSchema(Schema):
    id = fields.Str(dumps_only = True)
    body = fields.Str(required= True)
    user_id = fields.Str(required= True)

class UserSchema(Schema):
    id = fields.Str(dumps_only = True)
    username = fields.Str(required = True)
    email = fields.Str(required = True)
    password = fields.Str(required = True)
    first_name = fields.Str()
    last_name = fields.Str()
    address = fields.Str(required = True)
    Phone_number = fields.Str(required = True)
    required_services = fields.Str(required = True)

class UplateUserSchema(Schema):
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(required = True)
    new_password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    address = fields.Str()
    Phone_number = fields.Str()
    required_services = fields.Str()

class DeleteuserSchema (Schema):
    username = fields.Str(required = True)
    password = fields.Str(required = True)
