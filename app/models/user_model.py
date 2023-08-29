from flask_restx import fields

user_model = {
    'name': fields.String(required=True, description='Name'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
}