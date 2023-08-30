from flask import Flask
from flask_restx import Api, Resource, reqparse, Namespace
from app.databases import db, cursor
from .api.user import user_ns
from .config.jwt import jwt_config_info
from flask_jwt_extended import JWTManager
from .api.activity import activity_ns

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = jwt_config_info
jwt = JWTManager(app)

api = Api(app, version='1.0', title='MoWA API Document', description='Check the REST API specification of MoWA.')

# API에 네임스페이스 추가
api.add_namespace(user_ns)
api.add_namespace(activity_ns)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
