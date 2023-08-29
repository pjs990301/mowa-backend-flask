from flask_restx import fields
from datetime import datetime


def get_today_date():
    return datetime.now().date()


activity_model = {
    'email': fields.String(required=True, description='Email'),
    'date': fields.Date(default=get_today_date(), description='Date'),
    'warning_count': fields.Integer(default=0, description='Warning Count'),
    'activity_count': fields.Integer(default=0, description='Activity Count'),
    'fall_count': fields.Integer(default=0, description='Fall Count')
}
