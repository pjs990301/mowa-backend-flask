from flask_restx import Resource, Namespace, reqparse
from flask import request

from datetime import datetime
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
            모든 유저의 활동 조회
        """
        query = "SELECT email, date, warning_count, activity_count, fall_count FROM activity"
        cursor.execute(query)
        activitys = cursor.fetchall()
        activity_list = []

        for activity in activitys:
            activity_dict = {
                'email': activity[0],
                'date': activity[1].strftime('%Y-%m-%d'),
                'warning_count': activity[2],
                'activity_count': activity[3],
                'fall_count': activity[4],
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
            return {"message": "User not found with the provided email."}, 404

        query = ("INSERT INTO activity (id, email, date, warning_count, activity_count, fall_count) "
                 "VALUES (%s, %s, %s ,%s, %s, %s)")
        cursor.execute(query, (user_id_result[0], email, date, warning_count, activity_count, fall_count))
        db.commit()

        return {"message": "Activity data added successfully."}, 201


@activity_ns.route('/<string:user_email>')
class ActivityUserResource(Resource):
    def get(self, user_email):
        """
            특정 이메일을 통해 유저 활동 목록 조회
        """

        query = "SELECT date, warning_count,  activity_count, fall_count FROM activity WHERE email = %s"
        cursor.execute(query, (user_email,))
        activitys = cursor.fetchall()
        activity_list = []

        for activity in activitys:
            activity_dict = {
                'date': activity[0].strftime('%Y-%m-%d'),
                'warning_count': activity[1],
                'activity_count': activity[2],
                'fall_count': activity[3],
            }
            activity_list.append(activity_dict)
        return {'activitys': activity_list}, 200


@activity_ns.route('/<string:user_email>/stats/<int:year>/<int:month>')
class ActivityUserStatsResource(Resource):
    def get(self, user_email, year, month):
        """
            특정 이메일, 년월을 통해 유저 활동 통계 조회
        """
        query = ("SELECT YEAR(date) AS year, MONTH(date) AS month, email, "
                 "SUM(warning_count) AS warning_count, "
                 "SUM(activity_count) AS activity_count, "
                 "SUM(fall_count) AS fall_count "
                 "FROM activity "
                 "WHERE email = %s and YEAR(date)=%s and MONTH(date)=%s "
                 "GROUP BY YEAR(date), MONTH(date), email")

        cursor.execute(query, (user_email, year, month))
        activitys = cursor.fetchone()
        if activitys:
            activity_stats = {
                'email': activitys[2],
                'warning_count': int(activitys[3]),
                'activity_count': int(activitys[4]),
                'fall_count': int(activitys[5])
            }
            return activity_stats
        else:
            return {'message': 'Activitys not found.'}, 404


@activity_ns.route('/check/<string:user_email>')
class ActivityCheckResource(Resource):
    def post(self, user_email):
        """
            오늘 날짜의 데이터(행)가 없으면 새로운 데이터(행) 생성
        """
        query = "SELECT * FROM activity WHERE email = %s AND date = %s"
        cursor.execute(query, (user_email, datetime.now().date()))
        existing_entry = cursor.fetchone()

        if not existing_entry:
            fetch_id_query = "SELECT id FROM users WHERE email = %s"
            cursor.execute(fetch_id_query, (user_email,))
            user_id_result = cursor.fetchone()

            # Check if user exists with the given email
            if not user_id_result:
                return {"message": "User not found with the provided email."}, 404

            else:
                insert_query = ("INSERT INTO activity (id, email, date, warning_count, activity_count, fall_count)  "
                                "VALUES (%s, %s,%s, %s,%s, %s)")
                cursor.execute(insert_query, (user_id_result[0], user_email, datetime.now().date(), 0, 0, 0))
                db.commit()
                return {"message": "New entry created for the date."}, 201

        else:
            return {'message': 'Data already exists for the date.'}, 200


# @activity_ns.route('/<string:user_email>/<int:year>/<int:month>/<int:day>')
# class ActivityDetailResource(Resource):
#     def get(self, user_email, year, month, day):
#         """
#             특정 이메일의 년월일을 통해서 활동 조회
#         """
#         query = ("SELECT * FROM activity "
#                  "WHERE email = %s AND YEAR(date)=%s AND MONTH(date)=%s AND DAY(date)=%s")
#         cursor.execute(query, (user_email, year, month, day))
#         activity = cursor.fetchone()
#         if activity :
#             activity_stats = {
#
#             }
