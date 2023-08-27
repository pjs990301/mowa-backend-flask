from flask import Flask
from flask_restx import Api, Resource, reqparse, Namespace
from app.databases import db, cursor
from app.models import user_model

app = Flask(__name__)
api = Api(app, version='1.0', title='MoWA API Document', description='Check the REST API specification of MoWA.')

# 네임스페이스 생성
user_ns = Namespace('user', description='사용자 관련 기능', doc='/user', path='/user')

# 네임스페이스에 모델 등록
user_ns.models['UserModel'] = api.model('UserModel', user_model)

# API에 네임스페이스 추가
api.add_namespace(user_ns)


@user_ns.route('/signup')
class SignupResource(Resource):
    @api.expect(user_ns.models['UserModel'])
    def post(self):
        """
            유저 등록
        """
        data = api.payload
        name = data['name']
        email = data['email']
        password = data['password']

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
                'email': user[2]
            }
            user_list.append(user_dict)

        return {'users': user_list}


@user_ns.route('/user/<string:email>')
class UserResource(Resource):
    def get(self, email):
        """
            특정 이메일을 통해 유저 조회
        """
        # 주어진 이메일로 데이터베이스에서 사용자 정보 조회
        query = "SELECT id, name, email FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            user_dict = {
                'id': user[0],
                'name': user[1],
                'email': user[2]
            }
            return user_dict
        else:
            return {'message': 'User not found'}, 404

    @api.expect(user_ns.models['UserModel'])
    def put(self, email):
        """
            특정 이메일을 통해 유저 정보 수정
        """
        data = api.payload
        new_name = data['name']
        new_email = data['email']
        new_password = data['password']

        # 주어진 이메일로 기존 유저가 존재하는지 확인합니다.
        user_query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(user_query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # 사용자 정보 업데이트
            update_query = "UPDATE users SET name = %s, email = %s, password = %s WHERE email = %s"
            update_values = (new_name, new_email, new_password, email)

            cursor.execute(update_query, update_values)
            db.commit()

            return {'message': 'User information updated successfully'}, 200
        else:
            return {'message': 'No updates provided'}, 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
