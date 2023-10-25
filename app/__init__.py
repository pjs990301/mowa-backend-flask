from flask import Flask
from flask_mail import Mail
from flask_restx import Api, Resource, reqparse, Namespace

from app.config import *
from app.databases import db, cursor
from .api.user import user_ns
from .config.jwt import jwt_config_info, authorizations
from .api.activity import activity_ns

app = Flask(__name__)

app.config["SECRET_KEY"] = session_info['SECRET_KEY']

app.config["MAIL_SERVER"] = smtp_info['MAIL_SERVER']
app.config["MAIL_PORT"] = smtp_info['MAIL_PORT']
app.config["MAIL_USERNAME"] = smtp_info['MAIL_USERNAME']
app.config["MAIL_PASSWORD"] = smtp_info['MAIL_PASSWORD']
app.config["MAIL_USE_TLS"] = False if smtp_info['MAIL_USE_TLS'] == "False" else True
app.config["MAIL_USE_SSL"] = False if smtp_info['MAIL_USE_SSL'] == "False" else True
mail = Mail(app)


app.config["JWT_SECRET_KEY"] = jwt_config_info

api = Api(app, version='1.0', title='MoWA API Document', description='Check the REST API specification of MoWA.',
          authorizations=authorizations)

# API에 네임스페이스 추가
api.add_namespace(user_ns)
api.add_namespace(activity_ns)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
