import time
from datetime import datetime, timezone
from random import randint

from flask_mail import Message
from flask_restx import Resource, Namespace, reqparse
from flask import request, send_file, session
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import create_access_token

import os
import shutil

from app.models import *
from app.databases import db, cursor

import pymysql

# 네임스페이스 생성
user_ns = Namespace('User', description='사용자 관련 기능', doc='/user', path='/user')

user_field = user_ns.model('UserModel', user_model)
login_field = user_ns.model('LoginModel', login_model)

user_file_parser = reqparse.RequestParser()
user_file_parser.add_argument('profile_image', type=FileStorage, location='files')


@user_ns.route('/signup')
class SignupResource(Resource):
    @user_ns.expect(user_field, validate=True)
    def post(self):
        """
            유저 등록
        """
        if not request.is_json:
            return {"message": "Missing JSON in request."}, 400

        data = request.json

        required_keys = ['name', 'email', 'password']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        name = data['name']
        email = data['email']
        password = data['password']

        try:
            # Check if user with given email already exists
            user_query = "SELECT id FROM users WHERE email = %s"
            cursor.execute(user_query, (email,))
            existing_user = cursor.fetchone()
            cursor.fetchall()

            if existing_user:
                return {'message': 'User with this email already exists'}, 400

            # 사용자 정보 데이터베이스에 저장
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            values = (name, email, password)
            cursor.execute(query, values)
            db.commit()

            user_id = cursor.lastrowid
            access_token = create_access_token(identity=user_id)

            return {'message': 'User registered successfully', 'access_token': access_token}, 201

        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500


@user_ns.route('/login')
class LoginResource(Resource):
    @user_ns.expect(login_field, validate=True)
    def post(self):
        """
            유저 로그인
        """
        if not request.is_json:
            return {"message": "Missing JSON in request."}, 400

        data = request.json

        required_keys = ['email', 'password']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        email = data['email']
        password = data['password']

        try:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            cursor.fetchall()

            if user[3] != password:
                return {'message': 'Bad credentials'}, 401
            elif not user:
                return {'message': 'User not found'}, 404

            access_token = create_access_token(identity=user[0])

            return {'access_token': access_token}, 200

        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500


@user_ns.route('/users')
class UsersResource(Resource):
    def get(self):
        """
            모든 유저 조회
        """
        # 데이터베이스에서 모든 사용자 정보 조회
        try:
            query = "SELECT id, name, email FROM users"
            cursor.execute(query)
            users = cursor.fetchall()

            if not users:
                return {"message": "User not found."}, 404

            user_list = []
            for user in users:
                user_dict = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                }
                user_list.append(user_dict)

            return {'users': user_list}, 200

        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500


@user_ns.route('/<string:user_email>')
class UserResource(Resource):
    def get(self, user_email):
        """
            특정 이메일을 통해 유저 조회
        """
        try:
            # 주어진 이메일로 데이터베이스에서 사용자 정보 조회
            query = "SELECT id, name, email FROM users WHERE email = %s"
            cursor.execute(query, (user_email,))
            user = cursor.fetchone()
            cursor.fetchall()

            if user:
                user_dict = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2],
                }
                return {'user': user_dict}, 200
            else:
                return {'message': 'User not found'}, 404

        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500

    @user_ns.expect(user_field, validate=True)
    def put(self, user_email):
        """
            특정 이메일을 통해 유저 정보 수정
        """
        if not request.is_json:
            return {"message": "Missing JSON in request."}, 400

        data = request.json
        required_keys = ['name', 'email', 'password']
        if not all(key in data for key in required_keys):
            return {"message": "Missing required fields."}, 400

        new_name = data['name']
        new_email = data['email']
        new_password = data['password']

        try:
            # 주어진 이메일로 기존 유저가 존재하는지 확인합니다.
            user_query = "SELECT id FROM users WHERE email = %s"
            cursor.execute(user_query, (user_email,))
            existing_user = cursor.fetchone()
            cursor.fetchall()

            if new_email == user_email:
                return {'message': 'User can not change email address'}, 400

            if existing_user:

                # 사용자 정보 업데이트
                update_query = "UPDATE users SET name = %s, email = %s, password = %s WHERE email = %s"
                update_values = (new_name, new_email, new_password, user_email)

                cursor.execute(update_query, update_values)
                db.commit()

                return {'message': 'User information updated successfully'}, 200
            else:
                return {'message': 'User not found'}, 404
        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500

    def delete(self, user_email):
        """
            특정 이메일을 통해 유저 삭제
        """
        try:
            query = "SELECT id, name, email FROM users WHERE email = %s"
            cursor.execute(query, (user_email,))
            existing_user = cursor.fetchone()
            cursor.fetchall()

            if existing_user:
                user = {
                    'id': existing_user[0],
                    'name': existing_user[1],
                    'email': existing_user[2],
                }

                try:
                    delete_profile_dir = os.path.join("app", "profile_image", user['email'])
                    shutil.rmtree(delete_profile_dir)

                finally:
                    # 데이터베이스 ON DELETE CASCADE 옵션 설정
                    delete_user_query = "DELETE FROM users WHERE email = %s"
                    cursor.execute(delete_user_query, (user_email,))
                    db.commit()

                    return {'message': 'User deleted successfully'}, 200

            else:
                return {'message': 'User not found'}, 404

        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500


@user_ns.route('/<string:user_email>/profile')
class ProfileResource(Resource):
    @user_ns.doc(security='Bearer Auth')
    def get(self, user_email):
        """
            특정 이메일을 통해 유저 프로필 이미지 조회
        """
        try:
            user_query = "SELECT id, name, email FROM users WHERE email = %s"
            cursor.execute(user_query, (user_email,))
            existing_user = cursor.fetchone()
            cursor.fetchall()

            if existing_user:
                user = {
                    'id': existing_user[0],
                    'name': existing_user[1],
                    'email': existing_user[2],
                }

                profile_query = "SELECT id, email, src FROM profile WHERE email = %s"
                cursor.execute(profile_query, (user['email'],))
                profile = cursor.fetchone()
                cursor.fetchall()

                if profile:
                    return send_file(profile[2], mimetype='image/jpeg'), 200

                else:
                    return {'message': 'User profile image not found'}, 400

            else:
                return {'message': 'User not found'}, 404

        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500

    @user_ns.expect(user_file_parser, validate=True)
    def post(self, user_email):
        """
            특정 이메일을 통해 유저 프로필 이미지 추가
        """
        profile_image = user_file_parser.parse_args()['profile_image']
        try:
            # Check if user with given email already exists
            user_query = "SELECT id, name, email FROM users WHERE email = %s"
            cursor.execute(user_query, (user_email,))
            existing_user = cursor.fetchone()
            cursor.fetchall()

            if existing_user:
                user = {
                    'id': existing_user[0],
                    'name': existing_user[1],
                    'email': existing_user[2],
                }
                profile_query = "SELECT id FROM profile WHERE email = %s"
                cursor.execute(profile_query, (user['email'],))
                profile = cursor.fetchone()
                cursor.fetchall()

                if profile:
                    return {'message': 'User profile with this email already exists'}, 400

                if profile_image:
                    filename = secure_filename(profile_image.filename)
                    upload_dir = os.path.join("app", "profile_image", user['email'])
                    os.makedirs(upload_dir, exist_ok=True)
                    upload_path = os.path.join(upload_dir, filename)
                    profile_image.save(upload_path)
                    profile_image_db_path = os.path.join("profile_image", user['email'], filename)
                else:
                    return {'message': 'No profile image provided'}, 400

            else:
                return {'message': 'User not found'}, 404

            # 사용자 프로필 이미지 데이터베이스에 저장
            query = "INSERT INTO profile (id, email, src) VALUES (%s, %s, %s)"
            values = (user['id'], user['email'], profile_image_db_path)
            cursor.execute(query, values)
            db.commit()

            return {'message': 'User profile image registered successfully'}, 201

        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500

    @user_ns.expect(user_file_parser, validate=True)
    def put(self, user_email):
        """
            특정 이메일을 통해 유저 프로필 이미지 수정
        """
        profile_image = user_file_parser.parse_args()['profile_image']

        try:
            # Check if user with given email already exists
            user_query = "SELECT id, name, email FROM users WHERE email = %s"
            cursor.execute(user_query, (user_email,))
            existing_user = cursor.fetchone()
            cursor.fetchall()

            if existing_user:
                user = {
                    'id': existing_user[0],
                    'name': existing_user[1],
                    'email': existing_user[2],
                }

                if profile_image:
                    filename = secure_filename(profile_image.filename)
                    upload_dir = os.path.join("app", "profile_image", user['email'])
                    os.makedirs(upload_dir, exist_ok=True)
                    upload_path = os.path.join(upload_dir, filename)
                    profile_image.save(upload_path)
                    profile_image_db_path = os.path.join("profile_image", user['email'], filename)
                else:
                    return {'message': 'No profile image provided'}, 400
            else:
                return {'message': 'User not found'}, 404

            # 사용자 프로필 이미지 데이터베이스에 업데이트
            update_query = "UPDATE profile SET src = %s WHERE email = %s"
            cursor.execute(update_query, (profile_image_db_path, user['email']))
            db.commit()

            return {'message': 'Profile image updated successfully'}, 200
        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500

    def delete(self, user_email):
        """
            특정 이메일을 통해 유저 프로필 이미지 삭제
        """
        try:
            # Check if user with given email already exists
            user_query = "SELECT id, name, email FROM users WHERE email = %s"
            cursor.execute(user_query, (user_email,))
            existing_user = cursor.fetchone()
            cursor.fetchall()

            if existing_user:
                user = {
                    'id': existing_user[0],
                    'name': existing_user[1],
                    'email': existing_user[2],
                }

                profile_query = "SELECT id, email, src FROM profile WHERE email = %s"
                cursor.execute(profile_query, (user['email'],))
                profile = cursor.fetchone()
                cursor.fetchall()

                if profile:
                    remove_img_query = "UPDATE profile SET src = NULL WHERE email = %s"
                    cursor.execute(remove_img_query, (user['email'],))
                    db.commit()
                    return {'message': 'Profile image removed successfully'}, 200

                else:
                    return {'message': 'No profile image in Database'}, 400

            else:
                return {'message': 'User not found'}, 404
        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500


@user_ns.route('/emails')
class SendEmailUsingSMTP(Resource):
    def post(self):
        """
            특정 이메일을 통해 유저 이메일 인증
        """
        email_address = request.get_json(force=True)['email']
        otp_create_time = datetime.now()

        try:
            otp = generate_otp(email_address, otp_create_time)
            result = send_mail(email_address, otp)

            if result['statusCode'] == '202':
                return {'message': 'Email sent successfully'}, 200
            else:
                return {'message': 'Email sent failed'}, 400

        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500


@user_ns.route('/emails/verifications')
class VerifyEmailUsingSMTP(Resource):
    def post(self):
        email = request.get_json(force=True)['email']
        otp = request.get_json(force=True)['otp']

        session_otp = session.get(f'otp_{email}')
        session_time = session.get(f'time_{email}')

        if not session_otp or not session_time:
            return {'message': 'OTP not found'}, 404

        current_time = datetime.now(timezone.utc)

        if (current_time - session_time).total_seconds() > 180:
            session.pop(f'otp_{email}')
            session.pop(f'time_{email}')
            return {'message': 'OTP expired'}, 400

        if str(otp) == session_otp:
            session.pop(f'otp_{email}')
            session.pop(f'time_{email}')
            return {'message': 'OTP verified successfully'}, 200


@user_ns.route('/passwords')
class SendEmailForChangingPasswordUsingSMTP(Resource):
    def post(self):
        """
            특정 이메일을 통해 비밀번호 변경 인증
        """
        email_address = request.get_json(force=True)['email']
        otp_create_time = datetime.now()

        try:
            otp = generate_otp(email_address, otp_create_time)
            result = send_mail(email_address, otp)

            if result['statusCode'] == '202':
                return {'message': 'Email sent successfully'}, 200
            else:
                return {'message': 'Email sent failed'}, 400

        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500

    def patch(self):
        email_address = request.get_json(force=True)['email']
        new_password = request.get_json(force=True)['password']

        try:
            # Check if user with given email already exists
            user_query = "SELECT id FROM users WHERE email = %s"
            cursor.execute(user_query, (email_address,))
            existing_user = cursor.fetchone()
            cursor.fetchall()

            if existing_user:
                # 사용자 정보 업데이트
                update_query = "UPDATE users SET password = %s WHERE email = %s"
                update_values = (new_password, email_address)

                cursor.execute(update_query, update_values)
                db.commit()

                return {'message': 'User password updated successfully'}, 200
            else:
                return {'message': 'User not found'}, 404
        except pymysql.Error as e:
            return {"message": "Database error: {}".format(e)}, 500


@user_ns.route('/passwords/verifications')
class VerifyEmailForChaningPasswordUsingSMTP(Resource):
    def post(self):
        email = request.get_json(force=True)['email']
        otp = request.get_json(force=True)['otp']

        session_otp = session.get(f'otp_{email}')
        session_time = session.get(f'time_{email}')

        if not session_otp or not session_time:
            return {'message': 'OTP not found'}, 404

        current_time = datetime.now(timezone.utc)

        if (current_time - session_time).total_seconds() > 180:
            session.pop(f'otp_{email}')
            session.pop(f'time_{email}')
            return {'message': 'OTP expired'}, 400

        if str(otp) == session_otp:
            session.pop(f'otp_{email}')
            session.pop(f'time_{email}')
            return {'message': 'OTP verified successfully'}, 200


def send_mail(email, otp):
    import app
    mail = app.mail

    cert_info = {'email': email}
    email_address = cert_info['email']

    msg = Message("[MoWA] 이메일 인증번호", sender=app.config.smtp_info['MAIL_USERNAME'], recipients=[email_address])
    msg.body = '\n인증번호 : {}'.format(otp)
    mail.send(msg)
    response = {'statusCode': '202', 'statusName': 'success'}
    return response


def generate_otp(email_address, otp_create_time):
    otp = str(randint(100000, 999999))
    session[f'otp_{email_address}'] = otp
    session[f'time_{email_address}'] = otp_create_time
    return otp