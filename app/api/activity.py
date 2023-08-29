from flask_restx import Resource, Namespace, reqparse
from flask import request, send_file

import os

from app import api
from app.models import activity_model
from app.databases import db, cursor

activity_ns = Namespace('Activity', description='활동 통계 관련 기능', doc='/activity', path='/activity')

activity_field = activity_ns.model('ActivityModel', activity_model)


@activity_ns.route('/')
class ActivityResource(Resource):
    def get(self):
        """
            모든 유저의 활동 정보 조회
        """
        query = "SELECT id, email, date, warning_count, activity_count, fall_count FROM activity"
        cursor.execute(query)
        activitys = cursor.fetchall()
        activity_list = []

        for activity in activitys:
            activity_dict = {
                'id': activity[0],
                'email': activity[1],
                'date': activity[2].strftime('%Y-%m-%d'),
                'warning_count': activity[3],
                'activity_count': activity[4],
                'fall_count': activity[5],
            }
            activity_list.append(activity_dict)

        return {'activitys': activity_list}, 200

    @activity_ns.expect(activity_field, validate=True)
    def post(self):
        """
            유저의 활동 정보 추가
        """
        data = request.json
        email = data['email']
        date = data['date']
        warning_count = data['warning_count']
        activity_count = data['activity_count']
        fall_count = data['fall_count']

        fetch_id_query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(fetch_id_query, (email,))
        user_id_result = cursor.fetchone()

        # Check if user exists with the given email
        if not user_id_result:
            return {"error": "User not found with the provided email."}, 404

        query = ("INSERT INTO activity (id, email, date, warning_count, activity_count, fall_count) "
                 "VALUES (%s, %s, %s ,%s, %s, %s)")
        cursor.execute(query, (user_id_result[0], email, date, warning_count, activity_count, fall_count))
        db.commit()

        return {"message": "Activity data added successfully."}, 201
