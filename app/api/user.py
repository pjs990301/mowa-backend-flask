from flask_restx import Resource, Namespace, reqparse
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os

from app.models import user_model
from app.databases import db, cursor

# 네임스페이스 생성
user_ns = Namespace('user', description='사용자 관련 기능', doc='/user', path='/user')

# user_filed = user_ns.model('UserModel', user_model)

# Parser for parsing the request data
user_json_parser = reqparse.RequestParser()
user_json_parser.add_argument('name', type=str, required=True, help='Name is required')
user_json_parser.add_argument('email', type=str, required=True, help='Email is required')
user_json_parser.add_argument('password', type=str, required=True, help='Password is required')

user_file_parser = reqparse.RequestParser()
user_file_parser.add_argument('profile_image', type=FileStorage, location='files')

# TODO
""" 
1. 현재 회원가입 관련해서는 URL에 비밀번호가 노출되는 문제가 발생
   URL에 안 보이게 해야할 것으로 생각
   JSON 양식으로 하게 되면 Parser의 형태를 바꾸긴 해야할 것으로 생각
   JWT 도입 고려
2. 현재는 User Model 기반이 아닌 form-data URL을 통해서 Parser가 동작
   해당 부분에 대해서 User Model을 사용하는 게 바람직하다고 생각함
   그렇게 될 경우 File 받는 부분에 대해서 수정이 필요
   ⇒ 로직의 변화 필요
   File 받는 부분만 따로 분리할 것 인지 / 같이 진해할 것 인지 고려
"""


@user_ns.route('/signup')
class SignupResource(Resource):
    @user_ns.expect(user_json_parser, user_file_parser, validate=True)
    def post(self):
        """
            유저 등록
        """
        data = user_json_parser.parse_args()
        name = data['name']
        email = data['email']
        password = data['password']
        profile_image = user_file_parser.parse_args()['profile_image']

        # Check if user with given email already exists
        user_query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(user_query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            return {'message': 'User with this email already exists'}, 400

        # Save the profile image
        if profile_image:
            filename = secure_filename(profile_image.filename)
            upload_dir = os.path.join("app", "profile_image", name)
            os.makedirs(upload_dir, exist_ok=True)
            upload_path = os.path.join(upload_dir, filename)
            profile_image.save(upload_path)
            profile_image_db_path = os.path.join("app", "profile_image", name, filename)
        else:
            profile_image_db_path = None

        # 사용자 정보 데이터베이스에 저장
        query = "INSERT INTO users (name, email, password, profile_image) VALUES (%s, %s, %s, %s)"
        values = (name, email, password, profile_image_db_path)
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
        query = "SELECT id, name, email, profile_image FROM users"
        cursor.execute(query)
        users = cursor.fetchall()

        user_list = []
        for user in users:
            user_dict = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'profile_image': user[3]
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
        query = "SELECT id, name, email, profile_image FROM users WHERE email = %s"
        cursor.execute(query, (user_email,))
        user = cursor.fetchone()

        if user:
            user_dict = {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'profile_image': user[3]
            }
            return user_dict
        else:
            return {'message': 'User not found'}, 404

    @user_ns.expect(user_json_parser, validate=True)
    def put(self, user_email):
        """
            특정 이메일을 통해 유저 정보 수정
        """
        data = user_json_parser.parse_args()
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
