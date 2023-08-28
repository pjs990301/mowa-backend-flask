from flask_restx import Resource, Namespace, reqparse
from flask import request, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os

from app import api
from app.models import user_model
from app.databases import db, cursor

# 네임스페이스 생성
user_ns = Namespace('user', description='사용자 관련 기능', doc='/user', path='/user')

user_filed = user_ns.model('UserModel', user_model)

user_file_parser = reqparse.RequestParser()
user_file_parser.add_argument('profile_image', type=FileStorage, location='files')


@user_ns.route('/signup')
class SignupResource(Resource):
    @user_ns.expect(user_filed, validate=True)
    def post(self):
        """
            유저 등록
        """
        data = request.json
        name = data['name']
        email = data['email']
        password = data['password']

        # Check if user with given email already exists
        user_query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(user_query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return {'message': 'User with this email already exists'}, 400

        # 사용자 정보 데이터베이스에 저장
        query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        values = (name, email, password)
        cursor.execute(query, values)
        db.commit()

        return {'message': 'User registered successfully'}, 201


@user_ns.route('/users')
class UsersResource(Resource):
    def get(self):
        """
            모든 유저 조회
        """
        # 데이터베이스에서 모든 사용자 정보 조회
        query = "SELECT id, name, email FROM users"
        cursor.execute(query)
        users = cursor.fetchall()

        user_list = []
        for user in users:
            user_dict = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
            }
            user_list.append(user_dict)

        return {'users': user_list}


@user_ns.route('/<string:user_email>')
class UserResource(Resource):
    def get(self, user_email):
        """
            특정 이메일을 통해 유저 조회
        """
        # 주어진 이메일로 데이터베이스에서 사용자 정보 조회
        query = "SELECT id, name, email FROM users WHERE email = %s"
        cursor.execute(query, (user_email,))
        user = cursor.fetchone()

        if user:
            user_dict = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
            }
            return user_dict
        else:
            return {'message': 'User not found'}, 404

    @user_ns.expect(user_filed, validate=True)
    def put(self, user_email):
        """
            특정 이메일을 통해 유저 정보 수정
        """
        data = request.json
        new_name = data['name']
        new_email = data['email']
        new_password = data['password']

        # 주어진 이메일로 기존 유저가 존재하는지 확인합니다.
        user_query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(user_query, (user_email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # 사용자 정보 업데이트
            update_query = "UPDATE users SET name = %s, email = %s, password = %s WHERE email = %s"
            update_values = (new_name, new_email, new_password, user_email)

            cursor.execute(update_query, update_values)
            db.commit()

            return {'message': 'User information updated successfully'}, 200
        else:
            return {'message': 'User does not exist'}, 400


@user_ns.route('/<string:user_email>/profile')
class ProfileResource(Resource):
    def get(self, user_email):
        """
            특정 이메일을 통해 유저 프로필 이미지 조회
        """

        user_query = "SELECT id, name, email FROM users WHERE email = %s"
        cursor.execute(user_query, (user_email,))
        existing_user = cursor.fetchone()

        if existing_user:
            user = {
                'id': existing_user[0],
                'name': existing_user[1],
                'email': existing_user[2],
            }

            profile_query = "SELECT id, email, src FROM profile WHERE email = %s"
            cursor.execute(profile_query, (user['email'],))
            profile = cursor.fetchone()

            if profile:
                return send_file(profile[2], mimetype='image/jpeg')

            else:
                return {'message': 'User profile image not found'}, 400

        else:
            return {'message': 'User not found'}, 404

    @user_ns.expect(user_file_parser, validate=True)
    def post(self, user_email):
        """
            특정 이메일을 통해 유저 프로필 이미지 추가
        """
        profile_image = user_file_parser.parse_args()['profile_image']

        # Check if user with given email already exists
        user_query = "SELECT id, name, email FROM users WHERE email = %s"
        cursor.execute(user_query, (user_email,))
        existing_user = cursor.fetchone()

        if existing_user:
            user = {
                'id': existing_user[0],
                'name': existing_user[1],
                'email': existing_user[2],
            }

            if profile_image:
                filename = secure_filename(profile_image.filename)
                upload_dir = os.path.join("app", "profile_image", user['name'])
                os.makedirs(upload_dir, exist_ok=True)
                upload_path = os.path.join(upload_dir, filename)
                profile_image.save(upload_path)
                profile_image_db_path = os.path.join("profile_image", user['name'], filename)
            else:
                profile_image_db_path = None

        else:
            return {'message': 'User not found'}, 404

        # 사용자 프로필 이미지 데이터베이스에 저장
        query = "INSERT INTO profile (id, email, src) VALUES (%s, %s, %s)"
        values = (user['id'], user['email'], profile_image_db_path)
        cursor.execute(query, values)
        db.commit()

        return {'message': 'User profile image registered successfully'}, 201

    def put(self, user_email):
        """
            특정 이메일을 통해 유저 프로필 이미지 수정
        """

    def delete(self, user_email):
        """
            특정 이메일을 통해 유저 프로필 이미지 삭제
        """
